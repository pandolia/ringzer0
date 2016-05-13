import hashlib
import ringzer

def chall_func(hash_val, salt):
    for x in range(1000, 10000):
        if hashlib.sha1(str(x)+salt).hexdigest() == hash_val:
            return str(x)

ringzer.Challenge(57, chall_func)
