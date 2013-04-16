from .main_window import Ui_MainWindow
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QAbstractItemView, QMessageBox
from PyQt4.QtCore import SIGNAL
from sockserver import *
import time

class SomeoneConnected(QtCore.QThread):
    client = QtCore.pyqtSignal(object)
    def __init__(self, parent=None, server=None):
        super(SomeoneConnected, self).__init__(parent)
        self.serv=server
    
    def run(self):
        last = 0
        while True:
            time.sleep(0.5)
            if len([conn for conn in self.serv.conns])  != last:
                last = len(self.serv.conns)
                self.emit(SIGNAL("connected"))

class MainWindowWrapper(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #obsluga serwera
        self.serv = ConnsThreadingTCPServer((HOST,PORT), RequestHandler)
        self.serv_thread = threading.Thread(target = self.serv.serve_forever)
        self.serv_thread.daemon = True
        self.serv_thread.start() 
        
        self.connection_established = SomeoneConnected(server=self.serv)
        self.connection_established.start()
        self.connect(self.connection_established,SIGNAL("connected"),self.refresh_connections)
        self.ui.clientList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.connect(self.ui.getScreenFromSelected, SIGNAL("clicked()"), self.get_screen_from_selected)
        self.connect(self.ui.getAllScreen, SIGNAL("clicked()"), self.get_screen_from_all)
        self.connect(self.ui.disconnectSelected, SIGNAL("clicked()"), self.disconnect_selected)

    def on_quit(self):
        self.connection_established.quit()
        conns = [elem for elem in self.serv.conns]
        for conn in conns:
            conn.close_conn()
        self.serv.shutdown()

    def refresh_connections(self):
        self.ui.clientList.clear()
        for name in ["%d: %s" % (self.serv.conns.index(elem), elem.getinfo()) for elem in self.serv.conns]:
            QListWidgetItem(name, self.ui.clientList)
    
    def get_selected_items(self):
        selected = []
        for item in self.ui.clientList.selectedItems():
            selected.append(int(item.text().split(":")[0]))
        return selected

    def get_screen_from_selected(self):
        clients = ""
        for client in self.get_selected_items():
            self.serv.conns[client].getscreen()
            clients +=self.serv.conns[client].getinfo() + " "
        if clients:
            QMessageBox.information(self, "Pobrano", "Sprawdź " + clients, QMessageBox.Ok)

    def get_screen_from_all(self):
        for index in range(self.ui.clientList.count()):
            self.serv.conns[int(self.ui.clientList.item(index).text().split(":")[0])].getscreen()
        QMessageBox.information(self, "Pobrano", "Każdy klient wysłał screena", QMessageBox.Ok)

    def disconnect_selected(self):
        for client in self.get_selected_items():
           self.serv.conns[client].close_conn()
           self.serv.conns.pop(client)

