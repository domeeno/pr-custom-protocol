import json
import threading
import random
from logs.log import default_logger

from onion.transport_layer.handshake import HSHAKE_STATUS


def session(sck, client_address):
    default_logger.debug('New connection with: {}'.format(client_address))
    msg, addr = sck.recvfrom(128*1024)
    print("message: " + msg.decode())
    while True:
        msg, addr = sck.recvfrom(128*1024)
        if msg.decode() == 'exit':
            break
        default_logger.debug('client message is: {}'.format(msg.decode()))
        sck.sendto('sending request: {}'.format(msg.decode()).encode(), addr)
    default_logger.debug('{}'.format(client_address) + ' disconnected')
    client_address.close()


def add_connection(syn, addr, sck):
    workers = []

    data = '{ "sequence_number": %s, ' \
           '"status": %s }' % (syn.decode(), str(HSHAKE_STATUS.SYN_ACK.value))

    sck.sendto(data.encode('UTF-8'), addr)
    worker = threading.Thread(target=session, args=(sck, addr))
    workers.append(worker)

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()


# Client
def init_connection(server_host, server_port, socket):
    client_syn = str(random.randint(1000, 6000))
    status = HSHAKE_STATUS.SYN.value

    try:
        socket.sendto(client_syn.encode('utf-8'), (server_host, server_port))
    except Exception as e:
        default_logger.error("Couldn't connect to the server" + str(e))
        return client_syn, status

    data, addr = socket.recvfrom(128*1024)
    data = data.decode()
    recv = json.loads(data)
    print(str(recv['sequence_number']) + " : " + str(client_syn))
    if int(recv['sequence_number']) == int(client_syn):
        status = HSHAKE_STATUS.ACK.value
    return client_syn, status


# Client
def send_data(server_host, server_port, socket, syn):
    pass
