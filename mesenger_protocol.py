PREFIX_FIELD = (4, 1)
TYPES = ('m', "i")


def get_msg(s: 'socket'):
    prefix = receive(s, sum(PREFIX_FIELD)).decode()
    length, type_msg = prefix[:PREFIX_FIELD[0]], prefix[-1]
    if not (length.isdecimal() and type_msg in TYPES):
        return False
    msg = receive(s, int(length))
    return True, length, type_msg, msg


def send_msg(s: 'socket', data: "str,bytes", t: str = 'm'):
    if t == 'm':
        if type(data)!= str:
            data = str(data)
        s.send((str(len(data.encode())).zfill(PREFIX_FIELD[0]) + t + data).encode())


def receive(s: "socket", l: int) -> bytes:
    b = b''
    while len(b) < l:
        a = s.recv(l - len(b))
        if not a:
            raise ConnectionAbortedError
        b += a
    return b
