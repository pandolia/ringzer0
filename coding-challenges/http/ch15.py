import base64, hashlib
import ringzer

# https://ringzer0team.com/challenges/15
def chall_func(elf, checksum):    
    while elf[-1] != '\x7f':
        elf = base64.b64decode(elf)
    elf = elf[::-1]    
    if checksum == hashlib.md5(elf).hexdigest():
        return elf[1510:1514]+elf[1518:1520]

ringzer.Challenge(15, chall_func, chall_repeat = 5)
