#!/usr/bin/env python3.2
import socket, sys

def sendfile(filepath, addr = 'localhost', port = 25002):
    """Function for sending a file"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    with open(filepath, 'rb') as img:
        while True:
            file_stringed = img.read(1024)
            s.sendall(file_stringed)
            if not file_stringed:
                break
    s.close()

if __name__ == '__main__':
        sendfile(sys.argv[1])
