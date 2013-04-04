#!/usr/bin/env python2
import socket, sys, gtk.gdk, time
from subprocess import call

FREQUENCY = 20 #in seconds

def getscreen(name = "sc", ext = "png"):
    window = gtk.gdk.get_default_root_window()
    size = window.get_size()
    screen = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,size[0],size[1])
    screen = screen.get_from_drawable(window,window.get_colormap(),0,0,0,0,size[0],size[1])
    if (screen != None):
        filename = '.'.join([name,ext])
        screen.save(filename, ext)
        return filename
    return None

def sendfile(filepath, sock):
    """Function for sending a file"""
    with open(filepath, 'rb') as img:
        while True:
            file_stringed = img.read(1024)
            sock.sendall(file_stringed)
            if not file_stringed:
                break
    call(['rm', filepath])

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 25007))
    starttime = time.time()
    sendfile(getscreen(),s)
    while 1:
        if (time.time() - starttime) > FREQUENCY:
            sendfile(getscreen(),s)
            print("ok")
            starttime = time.time()
    s.close()
