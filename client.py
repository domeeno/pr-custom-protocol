import socket
import argparse

from logs.log import default_logger
from onion.transport_layer.handshake import HSHAKE_STATUS
from onion.transport_layer.connection import init_connection

parser = argparse.ArgumentParser(description="Client")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=20001)
args = parser.parse_args()

default_logger.debug('Connecting to server: {}:{}'.format(args.host, args.port))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # Try to establish connection
    (synchronize_sequence_number, status) = init_connection(args.host, args.port, sock)

    if status != HSHAKE_STATUS.ACK:
        sock.close()
        default_logger.debug("Client not Acknowledged: " + status)

    while status == HSHAKE_STATUS.ACK:
        msg = input()
        (synchronize_sequence_number, ack) = send_data(args.host, args.port, sock, synchronize_sequence_number)
        sock.sendto(msg.encode('utf-8'), (args.host, args.port))
        if msg == 'exit':
            default_logger.debug('Disconnected.')
            break
        (data, addr) = sock.recvfrom(128*1024)
        print(data.decode())
