import socket
import argparse

from logs.log import default_logger
from onion.application_level.atm import run_transaction
from onion.session_security.tls import tls_authenticate, tls_client_authenticate
from onion.transport_layer.enums.handshake import HSHAKE_STATUS
from onion.transport_layer.connection import init_connection
from onion.transport_layer.transmission import send_data

parser = argparse.ArgumentParser(description="Client")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=20001)
args = parser.parse_args()

default_logger.debug('Connecting to server: {}:{}'.format(args.host, args.port))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # Try to establish connection
    (synchronize_sequence_number, status, addr) = init_connection(args.host, args.port, sock)
    if status != HSHAKE_STATUS.ACK.value:
        sock.close()
        default_logger.debug("Client not Acknowledged: " + str(status))
    default_logger.info("Client connected to server.")

    is_authenticated, certificate, private_key = tls_client_authenticate(addr, sock)

    while status == HSHAKE_STATUS.ACK.value and is_authenticated:
        is_authenticated = run_transaction(addr, sock, synchronize_sequence_number, private_key, certificate)
