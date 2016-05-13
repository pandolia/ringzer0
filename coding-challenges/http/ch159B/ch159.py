import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import ringzer

import requests

def chall_func(hashval):
    return requests.Session().get("http://localhost/ch159-crack.php?sha1=" + hashval)._content

# posibility of match = 1.0-(63.0/64.0)**300 = 99.1%
ringzer.Challenge(159, chall_func, chall_repeat=300)
