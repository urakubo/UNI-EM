###
###
###

import sys, os, time, errno


import numpy as np
import copy
from distutils.dir_util import copy_tree
from itertools import chain


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")

sys.path.append(os.path.join(main_dir, "plugins", "miscellaneous"))
from TableGenerator import TableGenerator
from ThumbnailGenerator import ThumbnailGenerator

from Mzur  import Mzur
from Skimg  import Skimg

class Dialog_2D_Watershed(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "2D Watershed"
        self.initUI()


    def initUI(self):

        ##
        ## Define tab
        ##
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.resize(300, 500)


        # Add tabs
        mzur = Mzur(self.u_info)
        table1 = TableGenerator(self)
        thumb1 = ThumbnailGenerator(self)
        Widget1_bottom, obj_args, args = table1.GenerateTableObject(mzur)
        Widget1_top = thumb1.GenerateThumbnailObject(mzur, obj_args, args)  # Widget

        tab1 = QWidget()
        tab1.layout = QVBoxLayout(tab1)
        tab1.layout.addWidget(Widget1_top)
        tab1.layout.addWidget(Widget1_bottom)
        tab1.setLayout(tab1.layout)
        tabs.addTab(tab1, mzur.filter_name)


        sk = Skimg(self.u_info)
        table2 = TableGenerator(self)
        thumb2 = ThumbnailGenerator(self)
        Widget2_bottom, obj_args, args = table2.GenerateTableObject(sk)
        Widget2_top = thumb2.GenerateThumbnailObject(sk, obj_args, args)

        tab2 = QWidget()
        tab2.layout = QVBoxLayout(tab2)
        tab2.layout.addWidget(Widget2_top)
        tab2.layout.addWidget(Widget2_bottom)
        tab2.setLayout(tab2.layout)
        tabs.addTab(tab2, sk.filter_name)


        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()
