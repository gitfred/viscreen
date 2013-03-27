import socket, time

def reciever(port = 25002):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port)) #pusty string oznacza ze bierze localhost
    s.listen(1)
    conn, addr = s.accept()
    print(addr)
    data = ''
    o = open('testfile.jpg', 'wb+')
    rc=0
    while 1:
        try:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
            rc+=len(data);print rc
        except socket.errno, e:
            pass
        except IOError, e:
            pass
            #if e.errno == 32: 
             #   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              #  s.bind(('', port)) #pusty string oznacza ze bierze localhost
               # s.listen(1)
                #conn, addr = s.accept()
        o.write(data)
    o.close()
    conn.close()
    print("koniec")

if __name__ == '__main__':
    reciever()
