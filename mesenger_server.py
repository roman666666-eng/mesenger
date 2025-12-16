import socket as so
from collections import deque
import mesenger_protocol as pr

users = {}  # name:user
rooms = {}  # name:room
unadded = {}  # (ip,port):socket
s = so.socket()


def main():
    global unadded
    global users
    global rooms
    global s
    s.bind(('0.0.0.0', 60_001))
    s.listen()
    s.settimeout(0.01)
    rooms['main'] = room("main")


class user:
    def __init__(self, sock: 'socket', name: str, ad: tuple):
        self.socket = sock
        self.name = name
        self.addres = ad  # (ip,port)
        self.room = 'main'

    def __str__(self):
        return self.name

    def __eq__(self, us: 'user'):
        return type(self) == type(us) and self.addres == us.addres

    def reciv(self):
        w,l,t,msg = pr.get_msg(self.socket)
        if w:
            return msg

    def snd(self, msg: str):
        pr.send_msg(self.socket,msg)


class room:
    def __init__(self, name: str, us: list = None, ms: deque = None):
        self.usrs = us or []
        self.msgs = ms or deque()
        self.name = name

    def __add__(self, us: user):
        self.usrs.append(us)
        if self.name == 'main':
            self.msgs.append((us.name, f'\033[92mserver\033[0m: connected new user {us}'))
        elif len(self.usrs) > 1:
            self.msgs.append((us.name, f'\033[92mserver\033[0m: user {us} joined room {self.name}'))
        return self

    def sendall(self):
        while len(self.msgs):
            us, msg = self.msgs.popleft()
            print(msg)
            for j in self.usrs:
                if j.name != us:
                    j.snd(msg)


def close_command(s2: str) -> str:
    def levenshtein(s1: str) -> int:
        f = [[i + j if i * j == 0 else 0 for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                f[i][j] = f[i - 1][j - 1] if s1[i - 1] == s2[j - 1] else 1 + min(f[i][j - 1], f[i - 1][j],
                                                                                 f[i - 1][j - 1])
        return f[len(s1)][len(s2)]

    commands = (
        '!help', '!name', '!cls', '!private', '!create', '!join', '!exitroom', '!rooms', '!room', '!whoin', '!whoami')
    return min(commands, key=levenshtein)


if __name__ == '__main__':
    main()
