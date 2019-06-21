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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
from miscellaneous.TabGenerator import TabGenerator

icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))

sys.path.append(segmentation_dir)
from segment._2D_DNN.TrainingTab  import TrainingTab
from segment._2D_DNN.InferenceTab  import InferenceTab


class GenerateDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "2D DNN"
        self.initUI()


    def initUI(self):


        ##
        ## Define tab
        ##
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        tabs = QTabWidget()
        tabs.resize(300, 500)

        tab_source = TabGenerator(self)
        ##
        ## Training
        ##
        Training   = TrainingTab(self.u_info)
        tab1       = tab_source.GenerateTabWidget(Training) # Widget
        tabs.addTab(tab1, "Training")

        ##
        ## Inference
        ##
        Inference  = InferenceTab(self.u_info)
        tab2       = tab_source.GenerateTabWidget(Inference) # Widget
        tabs.addTab(tab2,"Inference")


        # Add tabs to widget
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)


        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()


