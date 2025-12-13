import socket as so
from collections import deque
import mesenger_protocol

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
        l = int(recive(self.socket, 3).decode())
        return recive(self.socket, l).decode()

    def snd(self, msg: str):
        self.socket.send((str(len(msg.encode())).zfill(3) + msg).encode())


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









if __name__ == '__main__':
    main()