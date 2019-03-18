#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#


from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import sys
import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir    = path.join(main_dir, "icons")
Plugins_dir = path.join(main_dir, "plugins")
sys.path.append(Plugins_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))

# from filesystem import *
# from gui import *
# from _dojo import *
# print(' global:', globals())

from MainWindow import MainWindow


if os.name == 'nt':
  try:
    import win32api
  except Exception:
    print('No win32api module.')


# end of class MyApp

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

