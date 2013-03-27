#!/usr/bin/env python3.2
import socket, time

def reciever(port = 25002):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port)) #pusty string oznacza ze bierze localhost
    s.listen(1)
    conn, addr = s.accept()
    print(addr)
    data = ''
    with open('testfile.jpg', 'wb+') as image:
        while True:
            data = conn.recv(1024)
            if not data: break
            image.write(data)
        conn.close()
    print("koniec")

if __name__ == '__main__':
    reciever()
