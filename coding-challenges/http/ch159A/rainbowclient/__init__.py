from socket import *

def tohashval(hashstr):
    return ''.join(chr(int(hashstr[i:i+2], 16)) for i in range(0, 40, 2))

def Lookup(host, port, hashstr):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(tohashval(hashstr))
    data = sock.recv(32)
    sock.close()
    if data and data[0] != '\x00':
        return data[1:]
