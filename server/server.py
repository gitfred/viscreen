#!/usr/bin/env python2
import socket, datetime, os

PORT = 25006

def reciever(sock):
    conn, addr = s.accept()
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    filepath = '%s/%s, %s.png' % (addr[0], addr[0], now)
    if not os.path.exists(addr[0]):
        os.makedirs(addr[0])
    with open(filepath, 'wb+') as image:
        while True:
            data = conn.recv(1024)
            if not data: break
            image.write(data)
    conn.close()
    print(filepath)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), PORT))
    s.listen(40)
    while 1:
        reciever(s)
