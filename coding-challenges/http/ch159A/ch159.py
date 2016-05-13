import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import ringzer

from rainbowclient import Lookup

def chall_func(hash_str):
    return Lookup('localhost', 9527, hash_str)

ringzer.Challenge(159, chall_func, 300)
