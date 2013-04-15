# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Apr 15 11:02:53 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(540, 284)
        MainWindow.setMaximumSize(QtCore.QSize(540, 284))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.clientList = QtGui.QListWidget(self.centralwidget)
        self.clientList.setGeometry(QtCore.QRect(30, 50, 256, 192))
        self.clientList.setObjectName(_fromUtf8("clientList"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.getScreenFromSelected = QtGui.QPushButton(self.centralwidget)
        self.getScreenFromSelected.setGeometry(QtCore.QRect(300, 60, 201, 27))
        self.getScreenFromSelected.setObjectName(_fromUtf8("getScreenFromSelected"))
        self.getAllScreen = QtGui.QPushButton(self.centralwidget)
        self.getAllScreen.setGeometry(QtCore.QRect(300, 100, 201, 27))
        self.getAllScreen.setObjectName(_fromUtf8("getAllScreen"))
        self.disconnectSelected = QtGui.QPushButton(self.centralwidget)
        self.disconnectSelected.setGeometry(QtCore.QRect(300, 140, 201, 27))
        self.disconnectSelected.setObjectName(_fromUtf8("disconnectSelected"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ViScreen", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Lista połączonych klientów", None, QtGui.QApplication.UnicodeUTF8))
        self.getScreenFromSelected.setText(QtGui.QApplication.translate("MainWindow", "Pobierz screena z zaznaczonych(ego)", None, QtGui.QApplication.UnicodeUTF8))
        self.getAllScreen.setText(QtGui.QApplication.translate("MainWindow", "Pobierz screena ze wszystkich", None, QtGui.QApplication.UnicodeUTF8))
        self.disconnectSelected.setText(QtGui.QApplication.translate("MainWindow", "Rozłącz zaznaczonych(ego)", None, QtGui.QApplication.UnicodeUTF8))

