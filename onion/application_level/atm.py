from logs.log import default_logger
from onion.transport_layer.enums.client_states import CLIENT_STATE, REQUEST_TYPE
from onion.transport_layer.transmission import send_data


def run_transaction(addr, sock, synchronize_sequence_number, private_key, certificate):
    state = CLIENT_STATE.IDLE
    print("Insert Card")
    client = "card1"
    state = CLIENT_STATE.CARD_INSERTED
    print("Card inserted")
    state = CLIENT_STATE.REQ_PIN
    while state == CLIENT_STATE.REQ_PIN:
        for i in range(3):
            print("Insert pin:")
            msg = input()
            synchronize_sequence_number, ack, state = send_data(addr, client, sock, synchronize_sequence_number,
                                                                private_key, certificate, state.value, msg)

            state, addr = sock.recvfrom(128 * 1024)
            if state.decode() == 'CLIENT_STATE.SUCCESS_PIN':
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
    state = CLIENT_STATE.ON_CLIENT_SESSION.value
    # MAKE TRANSACTIONS WHILE SIGNED IN WITH CARD AND PIN
    while state == CLIENT_STATE.ON_CLIENT_SESSION.value:
        print("1 - GET BALANCE, 2 - WITHDRAW, 3 - DEPOSIT")
        request = input()
        request = (int(request), )
        if request == REQUEST_TYPE.BALANCE.value:
            (synchronize_sequence_number, ack, state) = send_data(addr, client, sock, synchronize_sequence_number,
                                                                  private_key, certificate,
                                                                  CLIENT_STATE.ON_CLIENT_SESSION.value,
                                                                  "", request)
        else:
            print("AMOUNT:")
            amount = input()
            (synchronize_sequence_number, ack, state) = send_data(addr, client, sock, synchronize_sequence_number,
                                                                  private_key, certificate,
                                                                  CLIENT_STATE.ON_CLIENT_SESSION.value,
                                                                  amount, request)

        feedback, addr = sock.recvfrom(128 * 1024)

        if feedback == "exit":
            return False

        default_logger.info("Balance: " + feedback.decode())
