import socket

def reciever(port = 8765):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port)) #pusty string oznacza ze bierze localhost
    s.listen(1)
    conn, addr = s.accept()
    print(addr)
    
    while 1:
        data= conn.recv(1000000)
        if not data: break
        conn.sendall(data)
    open('testfile.jpg', 'w').write(data)
    conn.close()
