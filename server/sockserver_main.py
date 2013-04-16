#!/usr/bin/env python3
from GUI.sockserver_mainWrapper import MainWindowWrapper, QtGui
import sys

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindowWrapper()
    main_window.show()
    num = app.exec_()
    main_window.on_quit()
    sys.exit(num)
