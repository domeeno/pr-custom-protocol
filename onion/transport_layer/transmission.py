# Client
import json

from onion.application_level.message_protocol import message_structure
from onion.session_security.security import encrypt, decrypt
from onion.transport_layer.handshake import HSHAKE_STATUS


def send_data(addr, socket, syn, private_key):
    incremented_syn = int(syn) + 1
    msg = input()
    data = message_structure(addr, incremented_syn, HSHAKE_STATUS.ACK.value, msg)
    encrypted_data = str(encrypt(private_key, data)).strip()
    socket.sendto(encrypted_data.encode('UTF-8'), addr)
    return incremented_syn, HSHAKE_STATUS.ACK.value


def validate_recv_data(data_to_decrypt, public_key, trusted_ip, expected_syn):
    data_to_decrypt = list(eval(data_to_decrypt))

    decrypted_data = decrypt(public_key, data_to_decrypt)
    data = json.loads(decrypted_data)

    if str(data["source_ip"]) != str(trusted_ip) or int(data["syn"]) != int(expected_syn) or \
            int(data["ack"]) != HSHAKE_STATUS.ACK.value:
        return "error", data["source_ip"], data["syn"], False
    else:
        return data["message"], data["source_ip"], data["syn"], True
