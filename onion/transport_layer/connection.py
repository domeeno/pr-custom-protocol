import json
import random
import threading

from logs.log import default_logger
from onion.session_security.session import session
from onion.transport_layer.enums.handshake import HSHAKE_STATUS


def add_connection(sck):

    (syn, addr) = sck.recvfrom(128 * 1024)

    workers = []
    syn = syn.decode()

    data = '{ "sequence_number": %s, ' \
           '"status": %s }' % (syn, str(HSHAKE_STATUS.SYN_ACK.value))

    sck.sendto(data.encode('UTF-8'), addr)
    worker = threading.Thread(target=session, args=(addr, syn, sck))
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
    if int(recv['sequence_number']) == int(client_syn):
        status = HSHAKE_STATUS.ACK.value

    return client_syn, status, addr
