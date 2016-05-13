import ringzer
import hashlib

def chall_func(message):
    msg = ''.join(chr(int(message[i:i+8], 2)) for i in range(0, len(message), 8))
    return hashlib.sha512(msg).hexdigest()

ringzer.Challenge(14, chall_func)
