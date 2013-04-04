#!/usr/bin/env python2
import socket, datetime, os

def reciever(port = 25002):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port)) #pusty string oznacza ze bierze localhost
    s.listen(1)
    conn, addr = s.accept()
    print(addr)
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
    print("koniec")

if __name__ == '__main__':
    while 1:
        reciever()
