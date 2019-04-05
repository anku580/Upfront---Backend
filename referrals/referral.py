# import secrets
# import numpy as np
# from functools import partial
# import string

# def produce_amount_keys(amount_of_keys, _randint=np.random.randint):
#     keys = set()
#     pickchar = partial(secrets.choice, string.ascii_uppercase + string.digits)
#     while len(keys) < amount_of_keys:
#         keys |= {''.join([pickchar() for _ in range(_randint(6, 9))]) for _ in range(amount_of_keys - len(keys))}
#     return str(list(keys)[0])
import random
import string
def produce_amount_keys(No =1,stringLength=10):
    """Generate a random string of fixed length """
    letters= string.ascii_lowercase
    return ''.join(random.sample(letters,stringLength))