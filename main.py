#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
from PyQt5.QtWidgets import QApplication
import sys
import os
from os import path
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(os.path.join(main_dir, "gui"))

##
## Call UNI-EM main window.
##

from MainWindow import MainWindow


# end of class MyApp

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

