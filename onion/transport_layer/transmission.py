import json

from onion.transport_layer.enums.client_states import CLIENT_STATE, REQUEST_TYPE
from onion.transport_layer.message_structure import message_structure
from onion.session_security.crypto import encrypt, decrypt
from onion.transport_layer.enums.handshake import HSHAKE_STATUS
from server import pretty_idiotic_storage


def send_data(addr, client, socket, syn, private_key, certificate, state, msg, req=REQUEST_TYPE.NO_REQUEST.value):
    incremented_syn = int(syn) + 1
    data = message_structure(addr, client, incremented_syn, HSHAKE_STATUS.ACK.value, state, msg, certificate, req)
    encrypted_data = str(encrypt(private_key, data)).strip()
    socket.sendto(encrypted_data.encode('UTF-8'), addr)
    return incremented_syn, HSHAKE_STATUS.ACK.value


def validate_recv_data(data_to_decrypt, public_key, trusted_ip, expected_syn):
    from server import pretty_idiotic_storage

    data_to_decrypt = list(eval(data_to_decrypt))

    decrypted_data = decrypt(public_key, data_to_decrypt)
    data = json.loads(decrypted_data)

    if str(data["source_ip"]) != str(trusted_ip) or int(data["syn"]) != int(expected_syn) or \
            int(data["ack"]) != HSHAKE_STATUS.ACK.value:
        return "error", "Unknown", data["source_ip"], data["syn"], False, HSHAKE_STATUS.ERROR.value
    elif data["client"] not in pretty_idiotic_storage["clients"]:
        return "card invalid", data["client"], data["source_ip"], data["syn"], True, CLIENT_STATE.CLIENT_NOT_FOUND.value
    elif data["message"] != pretty_idiotic_storage[data["client"]]["pin"]:
        return "invalid pin", data["client"], data["source_ip"], data["syn"], True, CLIENT_STATE.ERROR_PIN.value
    else:
        return data["message"], data["client"], data["source_ip"], data["syn"], True, CLIENT_STATE.ON_CLIENT_SESSION.value


def complete_request(req, client, amount):
    balance = pretty_idiotic_storage["clients"][client]["balance"]

    if req == REQUEST_TYPE.BALANCE:
        return pretty_idiotic_storage["clients"][client]["balance"]

    if req == REQUEST_TYPE.WITHDRAW:
        pretty_idiotic_storage["clients"][client]["balance"] = balance - amount
        return pretty_idiotic_storage["clients"][client]["balance"]

    if req == REQUEST_TYPE.DEPOSIT:
        pretty_idiotic_storage["clients"][client]["balance"] = balance + amount
        return pretty_idiotic_storage["clients"][client]["balance"]
