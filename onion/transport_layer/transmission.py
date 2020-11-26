# Client
from onion.application_level.message_protocol import message_structure
from onion.session_security.security import encrypt


def send_data(addr, socket, syn, private_key):
    incremented_syn = int(syn) + 1
    msg = input()
    data = message_structure(addr, incremented_syn, True, msg)
    socket.sendto(encrypt(private_key, data).encode('UTF-8'), addr)


def validate_recv_data():
    pass
