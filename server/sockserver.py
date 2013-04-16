#!/usr/bin/env python3
import socket, socketserver, threading, datetime, os
from queue import Queue

HOST = 'localhost'
PORT = 9007

class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.q = Queue()
        self.addr = self.client_address
        self.host = socket.gethostbyaddr(self.addr[0])[0]
        self.name = threading.current_thread().name
        print("%s (%s) connected" % (self.host, self.addr))

    def handle(self):
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

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass,
                bind_and_activate)
        self.conns = []
        
    def process_request(self, request, client_address):
        socketserver.ThreadingMixIn.__init__(self, request, client_address)
        self.conns+=socketserver.ThreadingMixIn.t

    
if __name__ == '__main__':
    serv = ThreadedServer((HOST,PORT), RequestHandler)
    serv_thread = threading.Thread(target = serv.serve_forever)
    serv_thread.daemon = True
    serv_thread.start()


    while True:
        cmd = input("Type command: ")
        if cmd == 's':
            for elem in serv.conns:
                print(elem)

    serv.shutdown()


