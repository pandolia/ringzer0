import base64, itertools
import ringzer

def chall_func(hidden_xor_key, cpypted_msg):
    cpypted_msg = base64.b64decode(cpypted_msg)
    key_len = 10
    for i in range(0, len(hidden_xor_key)-key_len+1):
        xored = xor_str(cpypted_msg, hidden_xor_key[i:i+key_len])
        if all(map(is_valid_char, xored)):
            return xored

def xor_str(s, key):
    return ''.join(chr(ord(a)^ord(b)) for a, b in zip(s, itertools.cycle(key)))

def is_valid_char(c):
    return c.isalnum() or c == '-'

ringzer.Challenge(16, chall_func)
