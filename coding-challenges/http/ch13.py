import ringzer
import hashlib

def chall_func(message):
    return hashlib.sha512(message).hexdigest()

ringzer.Challenge(13, chall_func)
