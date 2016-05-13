import requests, re

USERNAME = '???'
PASSWORD = '???'
RINGZER_URL = 'https://ringzer0team.com'
LOGIN_URL = 'https://ringzer0team.com/login'
CSRF_PATTERN = re.compile(r"var \w+ = '(\w+)';")
SSHINFO_PATTERN = re.compile(r'<div class="challenge-wrapper">[^U]+User: (?P<username>\w+)[^P]+Password: (?P<password>\w+)[^h]+href="ssh://(?P<hostname>[\.\w]+):(?P<port>\d+)">')
SSHINFOS = {}

SESSION = None
def getSession():
    global SESSION
    if not SESSION:
        SESSION = requests.Session()
        html = SESSION.get(LOGIN_URL)._content
        SESSION.post(LOGIN_URL, data={
            'username' : USERNAME,
            'password' : PASSWORD,
            'csrf' : CSRF_PATTERN.search(html).group(1),
            'check' : 'true'
        })
    return SESSION

def GetSshInfo(chall_id):
    if chall_id in SSHINFOS:
        return SSHINFOS[chall_id]
    else:
        chall_url = '%s/challenges/%d' % (RINGZER_URL, chall_id)
        html = getSession().get(chall_url)._content
        sshinfo = SSHINFO_PATTERN.search(html).groupdict()
        sshinfo['port'] = int(sshinfo['port'])
        SSHINFOS[chall_id] = sshinfo
        return sshinfo

def SubmitFlag(chall_id, flag):
    chall_url = '%s/challenges/%d' % (RINGZER_URL, chall_id) 
    html = getSession().get(chall_url)._content
    html = getSession().post(chall_url, data={
        'id' : str(chall_id),
        'flag' : flag,
        'csrf' : CSRF_PATTERN.search(html).group(1),
        'check' : 'true'
    })
