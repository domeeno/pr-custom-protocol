# Client
import json

from onion.application_level.message_protocol import message_structure
from onion.session_security.security import encrypt, decrypt
from onion.transport_layer.handshake import HSHAKE_STATUS


def send_data(addr, socket, syn, private_key):
    incremented_syn = int(syn) + 1
    msg = input()
    data = message_structure(addr, incremented_syn, HSHAKE_STATUS.ACK.value, msg)
    socket.sendto(encrypt(private_key, data).encode('UTF-8'), addr)


def validate_recv_data(data_to_decrypt, public_key, trusted_ip, expected_syn):
    decrypted_data = decrypt(data_to_decrypt, public_key)
    data = json.loads(decrypted_data)

    if data["source_ip"] != trusted_ip or data["syn"] != expected_syn or data["ack"] != HSHAKE_STATUS.ACK.value:
        return "error", data["source_ip"], data["syn"], False
    else:
        return data["message"], data["source_ip"], data["syn"], True
