import json

from onion.session_security.crypto import encrypt, decrypt
from onion.transport_layer.enums.client_states import CLIENT_STATE, REQUEST_TYPE
from onion.transport_layer.enums.handshake import HSHAKE_STATUS
from onion.transport_layer.message_structure import message_structure

# A really dumb storage
pretty_idiotic_storage = {
    "clients": {"card1": {"pin": 3213, "balance": 1203.78},
                "card2": {"pin": 1111, "balance": 3212.32}
                }
}


def send_data(addr, client, socket, syn, private_key, certificate, state, msg, req=REQUEST_TYPE.NO_REQUEST.value):
    incremented_syn = int(syn) + 1
    data = message_structure(addr, client, incremented_syn, HSHAKE_STATUS.ACK.value, state, msg, certificate, req)
    encrypted_data = str(encrypt(private_key, data)).strip()
    socket.sendto(encrypted_data.encode('UTF-8'), addr)
    return incremented_syn, HSHAKE_STATUS.ACK.value, state


def validate_recv_data(data_to_decrypt, public_key, trusted_ip, expected_syn):

    data_to_decrypt = list(eval(data_to_decrypt))

    decrypted_data = decrypt(public_key, data_to_decrypt)
    data = json.loads(decrypted_data)

    if str(data["source_ip"]) != str(trusted_ip) or int(data["syn"]) != int(expected_syn) or \
            int(data["ack"]) != HSHAKE_STATUS.ACK.value:
        return "error", "Unknown", data["source_ip"], data["syn"], False, HSHAKE_STATUS.ERROR.value, data["req"]
    elif data["card"] not in pretty_idiotic_storage["clients"]:
        return "card invalid", data["card"], data["source_ip"], data["syn"], True, CLIENT_STATE.CLIENT_NOT_FOUND.value, data["req"]
    elif data["message"] != str(pretty_idiotic_storage["clients"][data["card"]]["pin"]) and data["s"] != "6":
        return "invalid pin", data["card"], data["source_ip"], data["syn"], True, \
               CLIENT_STATE.ERROR_PIN.value, data["req"]
    else:
        return data["message"], data["card"], data["source_ip"], data["syn"], True, \
               CLIENT_STATE.SUCCESS_PIN.value, data["req"]


def complete_request(req, client, amount):

    balance = pretty_idiotic_storage["clients"][client]["balance"]
    if req == str(REQUEST_TYPE.BALANCE.value):
        return "BALANCE: {}$".format(str(pretty_idiotic_storage["clients"][client]["balance"]))

    if req == str(REQUEST_TYPE.WITHDRAW.value):
        pretty_idiotic_storage["clients"][client]["balance"] = balance - int(amount)
        return "\nWITHDRAWN: {}$\nNEW BALANCE:{}$".format(amount, str(pretty_idiotic_storage["clients"][client]["balance"]))

    if req == str(REQUEST_TYPE.DEPOSIT.value):
        pretty_idiotic_storage["clients"][client]["balance"] = balance + int(amount)
        return "\nDEPOSITED: {}$\nNEW BALANCE:{}$".format(amount, str(pretty_idiotic_storage["clients"][client]["balance"]))

    if req == str(REQUEST_TYPE.NO_REQUEST.value):
        return None
