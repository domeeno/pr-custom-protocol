from logs.log import default_logger

from onion.session_security.tls import tls_authenticate, tls_verify_client
from onion.transport_layer.enums.client_states import CLIENT_STATE
from onion.transport_layer.transmission import validate_recv_data, complete_request


def session(client_address, client_syn, sck):
    default_logger.debug('New connection with: {}'.format(client_address))

    is_verified, certificate, public_key = tls_authenticate(client_address, sck)

    connection_ip, port = client_address
    current_ip = connection_ip
    current_syn = client_syn
    first_transaction = True
    transaction_session = False

    while str(connection_ip) == str(current_ip) and int(client_syn) == int(current_syn) and is_verified:
        current_syn = int(current_syn) + 1
        encrypted_msg, addr = sck.recvfrom(128 * 1024)

        is_verified = tls_verify_client(certificate, encrypted_msg, public_key)

        if not is_verified:
            default_logger.warning("Source not trustworthy. Source data: " + current_ip, current_syn)
            break

        msg, client, current_ip, client_syn, is_trusted, client_state, request_type =\
            validate_recv_data(encrypted_msg.decode(), public_key, current_ip, current_syn)

        if first_transaction:
            sck.sendto(str(CLIENT_STATE(client_state)).encode(), client_address)

        if client_state == CLIENT_STATE.CLIENT_NOT_FOUND.value:
            default_logger("Card {} not found".format(client))
            client_syn = client_syn
            continue

        if client_state == CLIENT_STATE.ERROR_PIN.value:
            default_logger.debug("{} pin error".format(client_address))
            client_syn = client_syn
            continue

        if not is_trusted:
            default_logger.warning("Source not trustworthy. Source data: " + current_ip, current_syn)
            break
        else:
            client_syn = current_syn

        if client_state == CLIENT_STATE.SUCCESS_PIN.value and first_transaction:
            sck.sendto("Pin success".encode(), client_address)
            first_transaction = False
            transaction_session = True

        if msg == 'exit':
            default_logger.debug('{}'.format(client_address) + ' disconnected')
            break

        if transaction_session:
            response = complete_request(request_type, client, msg)
            if response is not None:
                sck.sendto(str(response).encode(), client_address)
                default_logger.debug('client received the response: {}'.format(response))
