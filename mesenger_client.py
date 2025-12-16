import socket as so
from msvcrt import kbhit, getwch
from collections import deque
import os, datetime, sys
import mesenger_protocol
os.system('cls')
os.system('')
s = so.socket()
lastlength = 0
lastfstlength = 0



def printmsg(msg1: str, msg2: str = ''):
    global lastlength
    global lastfstlength
    print('\033[?25l', end='', flush=True)
    width, height = os.get_terminal_size()
    if lastfstlength // width > 0:
        print(f'\r\033[{lastfstlength // width}A', end='', flush=True)
    else:
        print('\r', end='', flush=True)
    if msglen(msg1 + msg2) > lastlength:
        print('\n' * (msglen(msg1 + msg2) // width - int(msglen(msg1 + msg2) % width == 0) + 1), end='', flush=True)
    else:
        print(' ' * lastlength, end='', flush=True)
    exp = msglen(msg1 + msg2) // width - int(msglen(msg1 + msg2) % width == 0) + 1 if msglen(
        msg1 + msg2) > lastlength else lastlength // width - int(lastlength % width == 0)
    if exp > 0:
        print(f'\r\033[{exp}A', end='', flush=True)
    else:
        print('\r', end='', flush=True)
    print(msg1 + msg2, end='', flush=True)
    if msglen(msg1 + msg2) // width - int(msglen(msg1 + msg2) % width == 0) > 0:
        print(f'\r\033[{msglen(msg1 + msg2) // width - int(msglen(msg1 + msg2) % width == 0)}A', end='', flush=True)
    else:
        print('\r', end='', flush=True)
    if msglen(msg1) // width - int(msglen(msg1) % width == 0) > 0:
        print(f'\033[{msglen(msg1) // width - int(msglen(msg1) % width == 0)}B', end='', flush=True)
    if msglen(msg1) % width != 0:
        print(f"\033[{msglen(msg1) % width}C", end='', flush=True)
    elif msglen(msg1) != 0:
        print(f'\033[1B\r', end='', flush=True)
    print('\033[?25h', end='', flush=True)
    lastlength = msglen(msg1 + msg2)
    lastfstlength = msglen(msg1)


def msglen(s: str) -> int:
    s = list(s)
    c = 0
    fl = False
    for i in s:
        if fl and i == 'm':
            fl = False
        elif i in ('\033', '\x1b'):
            fl = True
        elif not fl:
            c += 1
    return c