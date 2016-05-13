import paramiko, socket, select, re
import ringzerWEB

BLOCKSIZE = 1024
ASKEND = '\n'
ASKSEP = ' '
SEPLINE = '=' * 60
FLAGPATTERN = re.compile('FLAG-\w+')

class Channel:
    def __init__(self, chan):
        self.chan = chan
        chan.settimeout(0.0)
    
    def askone(self, message, expect='>'):
        if type(message) is not str:
            raise TypeError
        if message:
            try:
                self.chan.sendall(message+ASKEND)
            except socket.timeout:
                return ''
        return self.getreplies(1, expect)[0]
    
    def ask(self, messages, replysep='>'):
        if type(messages) is not list:
            raise TypeError
        try:
            self.chan.sendall(ASKSEP.join(str(x) for x in messages) + ASKEND)
        except socket.timeout:
            return [''] * len(messages)
        return self.getreplies(len(messages), replysep)
    
    def getreplies(self, n=1, replysep='>'):
        replies, buf = [], ''
        while len(replies) < n:
            data = ''
            select.select([self.chan], [], [])
            try:
                data = self.chan.recv(BLOCKSIZE)
            except socket.timeout:
                pass
            if not data:
                replies.append(buf)
                break
            buf += data
            curreplies = buf.split(replysep)
            buf = curreplies.pop()
            replies.extend(curreplies)
        replies.extend(['']*(n-len(replies)))
        return replies
    
    def close(self):
        return self.chan.close()

def SshChallenge(chall_id, chall_func, firstexpect='>', needinteract=False, password=None):
    print SEPLINE
    print 'Ringzer ssh challenge solver'
    print '    <https://ringzer0team.com/challenges/%d>' % chall_id
    print SEPLINE
    
    print '[+] Geting ssh server info from web page...',
    sshinfo = ringzerWEB.GetSshInfo(chall_id)
    if password:
        sshinfo['password'] = password
    print 'Done.\n    hostname={hostname}, port={port}'.format(**sshinfo)
    print '    username={username}, password={password}'.format(**sshinfo)
    
    print '[+] Login to ssh server...',
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    try:
        client.connect(**sshinfo)
        chan = Channel(client.invoke_shell())
    except:
        print 'Failed to login ssh server!!!'
        return
    print 'Done'
    
    print '[+] Start challenging'
    if needinteract:
        result = chall_func(chan)
    else:
        firstmessage = chan.askone('', firstexpect)
        result = chan.askone(chall_func(firstmessage))
    print '[+] Challenge done, result is:\n   ', result
    
    m = FLAGPATTERN.search(result)
    if m:
        print '    Challenge success!!!'
        print '[+] Submitting the flag...',
        try:
            ringzerWEB.SubmitFlag(chall_id, m.group(0))
            print 'Done'
        except:
            print '\n    Failed to auto commit the flag. You may commit it manual'        
    else:
        print '    Challenge failed!!!'
    print SEPLINE

    chan.close()

def GetSshChannel(chall_id, password=None):
    sshinfo = ringzerWEB.GetSshInfo(chall_id)
    if password:
        sshinfo['password'] = password
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    try:
        print 'xxx'
        client.connect(**sshinfo)
    except:
        print 'Failed to login ssh server!!!'
        return None
    return client.invoke_shell()
