import socket, time

def reciever(port = 8888):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port)) #pusty string oznacza ze bierze localhost
    s.listen(1)
    conn, addr = s.accept()
    print(addr)
    data = ''
    o = open('testfile.jpg', 'wb+')
    while 1:
        try:
            data = conn.recv(1024)
            conn.sendall(data)
        except socket.errno, e:
            pass
        except IOError, e:
            if e.errno == 32: 
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('', port)) #pusty string oznacza ze bierze localhost
                s.listen(1)
                conn, addr = s.accept()

        if not data: break
        o.write(data)
        print data
        
    o.close()
    conn.close()
    print("koniec")

if __name__ == '__main__':
    reciever()
