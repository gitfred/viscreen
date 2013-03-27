import socket, sys

def sendfile(filepath, addr = 'localhost', port = 25002):
    """Function for sending a file"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    o = open(filepath, 'rb')
    while 1:
        file_stringed = o.read(1024)
        s.sendall(file_stringed)
        data = s.recv(1024)
        if not data:break
    s.close();o.close()

if __name__ == '__main__':
        sendfile(sys.argv[1])
