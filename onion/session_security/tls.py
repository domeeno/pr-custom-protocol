import json

from onion.session_security.crypto import generate_keys, decrypt
from onion.session_security.enums.status import HSHAKE_STATUS
from onion.session_security.security_utils import rand_str


def tls_authenticate(client_address, sck):
    data, addr = sck.recvfrom(128*1024)

    if data.decode() == str(HSHAKE_STATUS.C_HELLO.value):
        sck.sendto(str(HSHAKE_STATUS.S_HELLO.value).encode(), client_address)
        certificate = rand_str()
        certificate_packet = '[{}, "{}"]'.format(str(HSHAKE_STATUS.CERTIFICATE.value), certificate)
        sck.sendto(str(certificate_packet).encode(), client_address)
    else:
        return False

    public_key, private_key = generate_keys()

    key_packet = '[{}, {}]'.format(str(HSHAKE_STATUS.S_KEY_EXCHANGE.value), private_key)
    sck.sendto(str(key_packet).encode(), client_address)
    sck.sendto(str(HSHAKE_STATUS.S_HELLO_DONE.value).encode(), client_address)

    data, addr = sck.recvfrom(128*1024)
    if data.decode() == str(HSHAKE_STATUS.CHANGE_TO_CYPHER.value):
        sck.sendto(str(HSHAKE_STATUS.AUTHENTICATED.value).encode(), client_address)
    else:
        return False

    return True, certificate, public_key


def tls_client_authenticate(server_addr, sck):
    key = ""

    sck.sendto(str(HSHAKE_STATUS.C_HELLO.value).encode(), server_addr)
    data, addr = sck.recvfrom(128*1024)
    if data.decode() == str(HSHAKE_STATUS.S_HELLO.value):
        data, addr = sck.recvfrom(128*1024)
    else:
        return False

    status, certificate = list(eval(data.decode()))

    if status == HSHAKE_STATUS.CERTIFICATE.value:
        data, addr = sck.recvfrom(128*1024)
        status, key = list(eval(data.decode()))
        if status == HSHAKE_STATUS.S_KEY_EXCHANGE.value:
            status, addr = sck.recvfrom(128*1024)
    else:
        return False

    if status.decode() == str(HSHAKE_STATUS.S_HELLO_DONE.value):
        sck.sendto(str(HSHAKE_STATUS.CHANGE_TO_CYPHER.value).encode(), server_addr)

    data, addr = sck.recvfrom(128*1024)

    return data.decode() == str(HSHAKE_STATUS.AUTHENTICATED.value), certificate, key


def tls_verify_client(certificate, encrypted_msg, public_key):
    data_to_decrypt = list(eval(encrypted_msg))

    decrypted_data = decrypt(public_key, data_to_decrypt)
    data = json.loads(decrypted_data)

    return str(data["certificate"]) == str(certificate)
