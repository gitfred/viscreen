import socket, sys

def sendfile(filepath, addr = 'localhost', port = 8888):
    """Function for sending a file"""
    o = open(filepath, 'rb')
    file_stringed = o.read()
    o.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    s.sendall(file_stringed)
    data = s.recv(1024)
    s.close()

if __name__ == '__main__':
        sendfile(sys.argv[1])
