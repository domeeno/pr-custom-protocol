import socket
import argparse

from logs.log import default_logger

parser = argparse.ArgumentParser(description="Client")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=20001)
args = parser.parse_args()

default_logger.debug('Connecting to server: {}:{}'.format(args.host, args.port))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    while True:
        msg = input()
        sock.sendto(msg.encode('utf-8'), (args.host, args.port))
        if msg == 'exit':
            default_logger.debug('Disconnected.')
            break
        (data, addr) = sock.recvfrom(128*1024)
        print(data.decode())
