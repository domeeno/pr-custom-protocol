import threading
import random
from logs.log import default_logger

from onion.transport_layer.handshake import HSHAKE_STATUS


def session(client_address, connection):
    default_logger.debug('New connection with: {}'.format(connection))
    while True:
        msg = client_address.recvfrom(128*1024)
        if msg.decode() == 'exit':
            break
        default_logger.debug('client message is: {}'.format(msg.decode()))
        client_address.sendall('sending request: {}'.format(msg.decode()).encode())
    default_logger.debug('{}'.format(connection) + ' disconnected')
    client_address.close()


def add_connection(syn, addr, sck):
    print("I arrived here")
    workers = []
    data = (syn + ":" + HSHAKE_STATUS.SYN_ACK)
    sck.sendto(data, addr)
    worker = threading.Thread(target=session, args=(addr, syn))
    workers.append(worker)

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()


# Client
def init_connection(server_host, server_port, socket):
    client_syn = str(random.randint(1000, 6000))
    status = HSHAKE_STATUS.SYN

    try:
        socket.sendto(client_syn.encode('utf-8'), (server_host, server_port))
    except Exception as e:
        default_logger.error("Couldn't connect to the server")

    (server_syn, status) = socket.recvfrom(128*1024)

    if server_syn == client_syn:
        status = HSHAKE_STATUS.ACK
    return client_syn, status


# Client
def send_data(server_host, server_port, socket, syn):
    pass
