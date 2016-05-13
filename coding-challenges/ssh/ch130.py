'''
> python ch130.py
============================================================
Ringzer ssh challenge solver
    <https://ringzer0team.com/challenges/130>
============================================================
[+] Geting ssh server info from web page... Done.
    hostname=ringzer0team.com, port=12643
    username=number, password=Z7IwIMRC2dc764L
[+] Login to ssh server... Done
[+] Start challenging
    7318 right. Won 1
    5683 right. Won 2
    3347 right. Won 3
    1170 right. Won 4
    5324 right. Won 5
     573 right. Won 6
    4349 right. Won 7
    9474 right. Won 8
    4041 right. Won 9
    2712 right. Won 10
[+] Challenge done, result is:
        You got the right number.

You beat the machine.
FLAG-????

    Challenge success!!!
[+] Submitting the flag... Done
============================================================
'''

from ringzerSSH import SshChallenge

def chall_func(chan):
    chan.askone('')
    i, restart = 0, True
    Base, InitDet = 16, 16**4
    while i < 10:
        if restart:
            Max, Det = InitDet-1, InitDet
            restart = False
        Min, Det = Max-Det, Det/Base
        if Det == 0:
            return 'Encountered unknow error, abort'
        numbers = range(Min+Det, Max, Det)
        replies = chan.ask(numbers)
        for number, reply in zip(numbers, replies):
            if not reply:
                return 'Encountered unknow error, abort'
            elif 'You got the right number' in reply:
                i += 1
                print '    %4d right. Won %d' % (number, i)
                if i == 10:
                    return reply
                restart = True
            elif (not restart) and ('too big' in reply):
                Max = number
                break

SshChallenge(130, chall_func, needinteract=True)
