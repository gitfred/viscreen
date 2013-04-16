#!/usr/bin/env python3
import socket, socketserver, threading, datetime, os, sys
from queue import Queue

HOST = 'localhost'
PORT = 9003
CONNS = []
class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.q = Queue()
        self.addr = self.client_address
        self.host = socket.gethostbyaddr(self.addr[0])[0]
        self.name = threading.current_thread().name
        print("%s (%s) connected" % (self.host, self.addr))

    def handle(self):
        CONNS.append(self)
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
        self.request.sendall(action.encode('utf-8'))
        filesize = self.request.recv(1024)
        if not filesize:
            self.q.put((None,None))
            print("client disconnected")
            return
        self.request.send(filesize) #odpowiadamy ty samym aby serwer wiedzial, ze juz moze wysylac
        filesize = int(filesize)
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        folder = '%s (%s)' % (self.host, self.addr[0])
        filepath = '%s/%s, %s.%s' % (folder, self.addr[0], now, extension)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(filepath, 'wb+') as image:
            recvsize = 0
            while recvsize<filesize:
                data = self.request.recv(1024)
                image.write(data)
                recvsize += len(data)
        print(filepath)

    def close_conn(self):
        self.q.put((None,None))
        self.request.sendall('disconnect'.encode('utf-8'))

        
    def getinfo(self):
        return "Host: %s IP: %s" % \
                (self.host, self.addr)

    def getscreen(self):
        self.q.put(('getscreen', 'png'))


if __name__ == '__main__':
    serv = socketserver.ThreadingTCPServer((HOST,PORT), RequestHandler)
    serv_thread = threading.Thread(target = serv.serve_forever)
    serv_thread.daemon = True
    serv_thread.start()


    while True:
        cmd = input("Type command: ")
        if cmd == 's':
            for elem in CONNS:
               print(elem.getinfo())
        elif cmd =='d':
            if CONNS:
                conns = ["%d: %s" % (CONNS.index(elem), elem.getinfo()) for elem in CONNS]
                for elem in conns:
                    print(elem)
                nr = int(input("Type client id: "))
                CONNS[nr].close_conn()
                del CONNS[nr]
            else:
                print("No clients connected")
        elif cmd == 'g':
            if CONNS:
                conns = ["%d: %s" % (CONNS.index(elem), elem.getinfo()) for elem in CONNS]
                for elem in conns:
                    print(elem)
                nr = int(input("Type client id: "))
                CONNS[nr].getscreen()
            else:
                print("No clients connected")
        elif cmd == 'q':
            if CONNS:
                for conn in CONNS:
                    conn.close_conn()

            serv.shutdown()
            sys.exit()



    serv.shutdown()


