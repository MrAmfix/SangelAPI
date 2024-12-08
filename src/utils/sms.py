from random import randint


def generate_code():
    return str(randint(1000000, 9999999))[1:]
