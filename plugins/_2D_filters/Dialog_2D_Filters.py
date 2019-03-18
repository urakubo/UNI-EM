###
###
###

import sys, os, time, errno


import numpy as np
import copy
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import subprocess as s
import tornado
import tornado.websocket


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
sys.path.append(os.path.join(main_dir, "plugins", "miscellaneous"))

from MiscellaneousPlugins  import MiscellaneousPlugins
from TableGenerator import TableGenerator
from ThumbnailGenerator import ThumbnailGenerator

from Gaussian import Gaussian
from Binary   import Binary
from Invert   import Invert
from Label   import Label
from Canny   import Canny

class Dialog_2D_Filters(QWidget, MiscellaneousPlugins):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "2D Filters"
        self.initUI()


    def initUI(self):
        ##
        ## Define tab
        ##
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.resize(300, 500)


        ##
        ## Generate smoothing tab
        ##
        sm = Gaussian(self.u_info)
        tabs   = self.AppendTab(tabs, sm)

        ##
        ## Generate binary tab
        ##
        b = Binary(self.u_info)
        tabs = self.AppendTab(tabs, b)

        ##
        ## Generate binary tab
        ##
        inv = Invert(self.u_info)
        tabs = self.AppendTab(tabs, inv)

        ##
        ## Generate labeling tab
        ##
        lbl = Label(self.u_info)
        tabs = self.AppendTab(tabs, lbl)

        ##
        ## Generate labeling tab
        ##
        can = Canny(self.u_info)
        tabs = self.AppendTab(tabs, can)


        ##
        ## Generate tabs
        ##

        layout.addWidget(tabs)
        self.setLayout(layout)


        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()


    def AppendTab(self, tabs, target_func):
            table1 = TableGenerator(self)
            thumb1 = ThumbnailGenerator(self)
            Widget1_bottom, obj_args, args = table1.GenerateTableObject(target_func) # Widget
            Widget1_top = thumb1.GenerateThumbnailObject(target_func, obj_args, args)  # Widget

            tab1 = QWidget()
            tab1.layout = QVBoxLayout(tab1)
            tab1.layout.addWidget(Widget1_top)
            tab1.layout.addWidget(Widget1_bottom)
            tab1.setLayout(tab1.layout)
            tabs.addTab(tab1, target_func.filter_name)

            return tabs

