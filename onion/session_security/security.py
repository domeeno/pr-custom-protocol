import random

from onion.session_security.security_utils import gcd, get_mult_inverse


def generate_keys():
    # To change
    p = 163
    q = 311

    n = p*q
    phi = (p-1)*(q-1)

    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = get_mult_inverse(e, phi)

    return (e, n), (d, n)


def encrypt(private_key, message_to_encrypt):
    key, n = private_key
    encrypted_message = [pow(ord(char), key) % n for char in message_to_encrypt]
    return encrypted_message


def decrypt(public_key, message_to_decrypt):
    key, n = public_key
    decrypted_message = [chr(pow(char, key) % n) for char in message_to_decrypt]
    return ''.join(decrypted_message)

# TODO Modify
# def generate_p():
#     return 163
#
#
# def generate_q():
#     return 311
# quick test
