import ringzer

def chall_func(shellcode):
    sc = shellcode.replace('\\', '0')
    return ''.join(chr(int(sc[i:i+4], 16) ^ 0xff) \
        for i in range(0x54*4, (0x54+0xc)*4, 4))

ringzer.Challenge(121, chall_func)
