import requests, re

USERNAME = '???'
PASSWORD = '???'
RINGZER_URL = 'https://ringzer0team.com'
LOGIN_URL = 'https://ringzer0team.com/login'
CSRF_PATTERN = re.compile(r"var \w+ = '(\w+)';")
MESSAGE_PATTERN = re.compile(r"----- [A-Za-z ]+ -----<br />\r\n\t\t([^\n]+)\n*<br />")
FLAG_PATTERN = re.compile(r">(FLAG-\w+)<")
SEPLINE = '=' * 100 + '\n'
SESSION = None

def Challenge(chall_id, chall_func, chall_repeat=1):
    chall_url = '%s/challenges/%d' % (RINGZER_URL, chall_id)
    print 'Ringzer challenge solver for <%s>' % chall_url
    print SEPLINE,
    for i in range(1, chall_repeat+1):
        print '[+] Try %dth round' % i
        try:
            flag = challenge(chall_id, chall_url, chall_func)
            if flag:
                print SEPLINE, 'Challenge success!!!', flag
                return flag
        except:
            print '\n    Encountered some unknown error, ignore it'
    print SEPLINE, 'Challenge Failured!!!'


def challenge(chall_id, chall_url, chall_func):
    global SESSION

    if not SESSION:
        print '    Login...',       
        SESSION = requests.Session()
        html = SESSION.get(LOGIN_URL)._content
        SESSION.post(LOGIN_URL, data={
            'username' : USERNAME,
            'password' : PASSWORD,
            'csrf' : CSRF_PATTERN.search(html).group(1),
            'check' : 'true'
        })
        print 'Done, login as: %s' % USERNAME
    else:
        print '    Already logined'

    print '    Getting challenge messages...',
    html = SESSION.get(chall_url)._content
    messages = MESSAGE_PATTERN.findall(html)
    print 'Done, messages are: %s' % messages
    
    print '    Finding the answer...', 
    answer = chall_func(*messages)
    if not answer:
        print 'Failure to find the answer!'
        return
    print 'Done, the answer is: %s' % answer
    
    print '    Sending the answer...',
    html = SESSION.get(chall_url+'/'+answer)._content
    flag = FLAG_PATTERN.search(html)
    if not flag:
        print 'Wrong answer or too slow!'
        return
    else:
        flag = flag.group(1)
    print 'Done, got the flag: %s' % flag
    
    print '    Submitting the flag...',
    try:            
        html = SESSION.post(chall_url, data={
            'id' : str(chall_id),
            'flag' : flag,
            'csrf' : CSRF_PATTERN.search(html).group(1),
            'check' : 'true'
        })
        print 'Done.'
    except:
        print 'Failure to auto submit the flag. You may submit it manual.'
    
    return flag
