import ringzer

def chall_func(message):
    ops = message.split()
    return str(int(ops[0]) + int(ops[2], 16) - int(ops[4], 2))

ringzer.Challenge(32, chall_func)

