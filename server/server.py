#!/usr/bin/env python2
import socket, datetime, os, select, sys
from threading import Thread

PORT = 9001

class ConnectionHandler(Thread):

    def __init__(self, sock, addr):
        Thread.__init__(self)
        self.sock = sock
        self.addr = addr

    def run(self):
        while True:
            filesize = self.sock.recv(1024)
            self.sock.send(filesize)
            filesize = int(filesize)
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            folder = '%s (%s)' % (socket.gethostbyaddr(self.addr[0])[0], self.addr[0])
            filepath = '%s/%s, %s.png' % (folder, self.addr[0], now)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(filepath, 'wb+') as image:
                recvsize = 0
                while recvsize<filesize:
                    data = self.sock.recv(1024)
                    image.write(data)
                    recvsize += len(data)
            print(filepath)
        self.sock.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(40)
    while 1:
        ch = ConnectionHandler(*s.accept())
        ch.start()
