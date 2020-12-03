import random
import string


def rand_str(chars=string.ascii_uppercase + string.digits + string.ascii_lowercase, n=7):
    return ''.join(random.choice(chars) for _ in range(n))


def gen_primes(low, up):
    primes = [i for i in range(low, up) if is_prime(i)]
    return random.choice(primes)


def is_prime(x):
    count = 0
    for i in range(int(x/2)):
        if x % (i+1) == 0:
            count = count+1
    return count == 1


# Greatest common denominator
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Euclid algorithm for finding multiplicative inverse
def get_mult_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi
