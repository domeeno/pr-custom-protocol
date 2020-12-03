import socket
import argparse

from logs.log import default_logger
from onion.transport_layer.connection import add_connection

parser = argparse.ArgumentParser(description="Server")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=20001)
args = parser.parse_args()


sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sck.bind((args.host, args.port))
    default_logger.debug(f"Running server on: {args.host}:{args.port}")
    default_logger.info('Server {}:{} ready to use.\n\n'.format(args.host, args.port))
except Exception as e:
    default_logger.warning(str(e) + " host: {}:{}".format(args.host, args.port))
    raise SystemExit(f"Couldn't bind the server on host: {args.host}:{args.port}")

while True:
    try:
        add_connection(sck=sck)
    except KeyboardInterrupt as e:
        default_logger.debug('Shutting down server')
    except Exception as e:
        default_logger.debug(e)
