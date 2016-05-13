import random, itertools
N = 18
s = list('0123456789abcdefghijklmnopqrstuvwxyz')
random.shuffle(s)
for x in itertools.product(s[:N], repeat=6):
    print ''.join(x)
