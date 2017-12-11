import random
import string


def get_yz_code(count):
    return "".join(random.sample(string.ascii_uppercase + string.digits + string.ascii_lowercase, count))


[print(get_yz_code(4)) for x in range(0, 1000)]
