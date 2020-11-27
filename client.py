import socket
import argparse

from logs.log import default_logger
from onion.application_level.client_interface import client_intro
from onion.transport_layer.handshake import HSHAKE_STATUS
from onion.transport_layer.connection import init_connection
from onion.transport_layer.transmission import send_data

parser = argparse.ArgumentParser(description="Client")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=20001)
args = parser.parse_args()

default_logger.debug('Connecting to server: {}:{}'.format(args.host, args.port))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # Try to establish connection
    (synchronize_sequence_number, status, addr, private_key_holder) = init_connection(args.host, args.port, sock)

    if status != HSHAKE_STATUS.ACK.value:
        sock.close()
        default_logger.debug("Client not Acknowledged: " + str(status))
    default_logger.info("Client connected to server.")

    private_key = list(eval(private_key_holder))

    while status == HSHAKE_STATUS.ACK.value:
        client_intro()
        (synchronize_sequence_number, ack) = send_data(addr, sock, synchronize_sequence_number, private_key)
        (data, addr) = sock.recvfrom(128 * 1024)
        print(data.decode())
