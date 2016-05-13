import hashlib
import ringzer

def chall_func(hash_val):
    for x in range(1000, 10000):
        if hashlib.sha1(str(x)).hexdigest() == hash_val:
            return str(x)

ringzer.Challenge(56, chall_func)
