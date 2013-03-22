import socket

def sendfile(filepath, addr = 'localhost', port = 8765):
    """Function for sending a file"""
    file_stringed = open(filepath, 'U').read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    s.sendall(file_stringed)

