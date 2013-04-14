from .main_window import Ui_MainWindow
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QAbstractItemView
from PyQt4.QtCore import SIGNAL
from server import *
import time

class SomeoneConnected(QtCore.QThread):
    client = QtCore.pyqtSignal(object)
    def __init__(self, parent=None, server=None):
        super(SomeoneConnected, self).__init__(parent)
        self.serv=server
    
    def run(self):
        last = 0
        while True:
            time.sleep(2)
            if len(self.serv.conns) != last:
                last = len(self.serv.conns)
                self.emit(SIGNAL("connected"))

class MainWindowWrapper(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.serv = Server()
        self.serv.start()
        self.connection_established = SomeoneConnected(server=self.serv)
        self.connection_established.start()
        self.connect(self.connection_established,SIGNAL("connected"),self.refresh_connections)
        self.ui.clientList.setSelectionMode(QAbstractItemView.MultiSelection)
    
    def on_quit(self):
        self.connection_established.quit()
        conns = [elem for elem in self.serv.conns if elem.isAlive()]
        for conn in conns:
            conn.close_conn()
        self.serv.shutdown_serv()

    def refresh_connections(self):
        self.ui.clientList.clear()
        for name in [elem.getinfo() for elem in self.serv.conns]:
            QListWidgetItem(name, self.ui.clientList)

