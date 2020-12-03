from logs.log import default_logger
from onion.transport_layer.enums.client_states import CLIENT_STATE, REQUEST_TYPE
from onion.transport_layer.transmission import send_data, make_requests


def run_transaction(addr, sock, synchronize_sequence_number, private_key, certificate):
    print("Insert Card")
    client = "card1"
    state = CLIENT_STATE.CARD_INSERTED.value
    print("Card inserted")
    state = CLIENT_STATE(state + 1)
    while state == CLIENT_STATE.REQ_PIN:
        for i in range(3):
            print("Insert pin:")
            msg = input()
            (synchronize_sequence_number, ack, state) = send_data(addr, client, sock, synchronize_sequence_number,
                                                                  private_key, certificate, state.value, msg)

            state, addr = sock.recvfrom(128 * 1024)

            if state == str(CLIENT_STATE.SUCCESS_PIN.value):
                state = CLIENT_STATE.SUCCESS_PIN
                break
            else:
                default_logger.warning("Pin error {} more tries".format(3 - i))
                state = CLIENT_STATE.ERROR_PIN

    if state == CLIENT_STATE.ERROR_PIN:
        default_logger.info("Client locked out")
        sock.close()
        return

    data, addr = sock.recvfrom(128 * 1024)
    default_logger.info(data.decode())

    # MAKE TRANSACTIONS WHILE SIGNED IN WITH CARD AND PIN
    while state == str(CLIENT_STATE.ON_CLIENT_SESSION.value):
        request = input()
        if str(request) == str(REQUEST_TYPE.BALANCE.value):
            (synchronize_sequence_number, ack, state) = send_data(addr, client, sock, synchronize_sequence_number,
                                                                  private_key, certificate, CLIENT_STATE.ON_CLIENT_SESSION.value,
                                                                  "", request)
        else:
            amount = input()
            (synchronize_sequence_number, ack, state) = send_data(addr, client, sock, synchronize_sequence_number,
                                                                  private_key, certificate, CLIENT_STATE.ON_CLIENT_SESSION.value,
                                                                  amount, request)

        feedback, addr = sock.recvfrom(128*1024)
        default_logger.info("Balance: " + feedback.decode())
