import json
import threading
import random
from logs.log import default_logger
from onion.session_security.security import generate_keys

from onion.transport_layer.handshake import HSHAKE_STATUS
from onion.transport_layer.transmission import validate_recv_data


def session(client_address, client_syn, public_key, sck):
    default_logger.debug('New connection with: {}'.format(client_address))

    connection_ip, port = client_address
    current_ip = connection_ip
    current_syn = client_syn

    while str(connection_ip) == str(current_ip) and int(client_syn) == int(current_syn):
        current_syn = int(current_syn) + 1
        encrypted_msg, addr = sck.recvfrom(128*1024)
        msg, current_ip, client_syn, is_trusted = validate_recv_data(encrypted_msg.decode(), public_key,
                                                                      current_ip, current_syn)
        
        if not is_trusted:
            default_logger.warning("Source not trustworthy. Source data: " + current_ip, current_syn)
            break
        else:
            client_syn = current_syn

        if msg == 'exit':
            default_logger.debug('{}'.format(client_address) + ' disconnected')
            break

        default_logger.debug('client message is: {}'.format(msg))
        sck.sendto('sending request: {}'.format(msg).encode(), addr)

    sck.close()


def add_connection(syn, addr, sck):
    workers = []
    syn = syn.decode()
    public_key, private_key = generate_keys()

    data = '{ "sequence_number": %s, ' \
           '"status": %s,' \
           '"private_key": "%s" }' % (syn, str(HSHAKE_STATUS.SYN_ACK.value), str(private_key))

    sck.sendto(data.encode('UTF-8'), addr)
    worker = threading.Thread(target=session, args=(addr, syn, public_key, sck))
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
    print(data)
    data = data.decode()
    recv = json.loads(data)
    print(str(recv['sequence_number']) + " : " + str(client_syn))
    if int(recv['sequence_number']) == int(client_syn):
        status = HSHAKE_STATUS.ACK.value
    return client_syn, status, addr, recv['private_key']
