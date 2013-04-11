#!/usr/bin/env python2
import socket, datetime, os, select, sys
from threading import Thread
from Queue import Queue

PORT = 9005

class Server(Thread):
    """
    Watek obslugujacy serwer
    """

    def __init__(self, port=PORT):
        Thread.__init__(self)
        self.port=port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conns = []
        self.sock.bind(('', self.port))
        self.sock.listen(40)
        self.sock.settimeout(2) #ustawiony timeout na 5 sekund, aby accept sie nie blokowal
        self.is_online = True

    def run(self):
        while self.is_online:
            try:
                c = Connection(len(self.conns), *self.sock.accept())
                c.start()
                self.conns.append(c)
            except socket.timeout:
                continue
        self.sock.close()
        

    def close_conn(self, id_client):
        self.conns[id_client].close_conn()

    def getscreen(self, id_client):
        self.conns[id_client].q.put(('getscreen', 'png'))

    def shutdown_serv(self):
        self.is_online = False

class Connection(Thread):
    """
    Watek obslugujacy wybrane polaczenie z serwerem
    """

    def __init__(self, id_client, sock, addr):
        Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.id_client = id_client
        self.host = socket.gethostbyaddr(self.addr[0])[0]
        self.q = Queue()
        print("\n%s connected" % self.host)

    def run(self):
        while True:
            action, extension = self.q.get()
            if not action:
                break
            self.recievefile(action, extension)
            self.q.task_done()

    def recievefile(self, action, extension):
        """
        Przyjmuje jakiekolwiek pliki za pomoca aciton,
        zapisuje z wybranym rozszerzeniem
        """
        self.sock.sendall(action)
        filesize = self.sock.recv(1024)
        if not filesize:
            self.q.put((None,None))
            print("KLIENT SIE ROZLACZYL!!!")
            return
        self.sock.send(filesize) #odpowiadamy ty samym aby serwer wiedzial, ze juz moze wysylac
        filesize = int(filesize)
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        folder = '%s (%s)' % (self.host, self.addr[0])
        filepath = '%s/%s, %s.%s' % (folder, self.addr[0], now, extension)
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
        self.q.put((None,None)) #wrzucamy do kolejki sygnal konca
        self.sock.sendall('disconnect')
        

    def getinfo(self):
        return "Client ID: %d Host: %s IP: %s" % \
                (self.id_client, self.host, self.addr)

if __name__ == '__main__':

    serv = Server()
    serv.start()

    print("Options: getscreen [g] lista [s] and disconnect [d] quit [q]\n")
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
