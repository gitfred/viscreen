#!/usr/bin/env python2
import socket, datetime, os
from threading import Thread

PORT = 25007

class ConnectionHandler(Thread):

    def __init__(self, sock, addr):
        Thread.__init__(self)
        self.sock = sock
        self.addr = addr

    def run(self):
        while True:
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            filepath = '%s/%s, %s.png' % (self.addr[0], self.addr[0], now)
            if not os.path.exists(self.addr[0]):
                os.makedirs(self.addr[0])
            with open(filepath, 'wb+') as image:
                while True:
                    data = self.sock.recv(1024)
                    if not data: break
                    image.write(data)
            print(filepath)
        self.sock.close()

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
        conn, addr = s.accept()
        ch = ConnectionHandler(conn, addr)
        ch.run()
