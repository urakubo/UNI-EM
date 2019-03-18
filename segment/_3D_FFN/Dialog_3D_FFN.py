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
import glob

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")

from TableGeneratorFFN import TableGeneratorFFN
from ThumbnailGeneratorFFN import ThumbnailGeneratorFFN
from FFNPrepTraining   import FFNPrepTraining
from FFNTraining    import FFNTraining
from FFNInference   import FFNInference
from FFNPostprocessing   import FFNPostprocessing

segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)


class Dialog_3D_FFN(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "3D FFN"
        self.initUI()


    def initUI(self):
        ##
        ## Define tab
        ##
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.resize(300, 500)

        ##
        ## Prepare FFN training
        ##
        prep_ffn = FFNPrepTraining(self.u_info)

        table1 = TableGeneratorFFN(self)
        thumb1 = ThumbnailGeneratorFFN(self)
        Widget1_bottom, obj_args, args = table1.GenerateTableObject(prep_ffn) # Widget
        Widget1_top = thumb1.GenerateThumbnailObject(prep_ffn, obj_args, args)  # Widget

        tab1 = QWidget()
        tab1.layout = QVBoxLayout(tab1)
        tab1.layout.addWidget(Widget1_top)
        tab1.layout.addWidget(Widget1_bottom)
        tab1.setLayout(tab1.layout)
        tabs.addTab(tab1, 'Preprocessing')

        ##
        ## FFN training
        ##
        run_ffn = FFNTraining(self.u_info)
        table2 = TableGeneratorFFN(self)
        Widget2_bottom, obj_args, args = table2.GenerateTableObject(run_ffn) # Widget
        tabs.addTab(Widget2_bottom, 'Training')

        ##
        ## FFN inferernce
        ##
        run_ffn = FFNInference(self.u_info)
        table3 = TableGeneratorFFN(self)
        Widget3_bottom, obj_args, args = table3.GenerateTableObject(run_ffn) # Widget
        tabs.addTab(Widget3_bottom, 'Inference')

        ##
        ## FFN postprocessing
        ##
        run_ffn = FFNPostprocessing(self.u_info)
        table4 = TableGeneratorFFN(self)
        Widget4_bottom, obj_args, args = table4.GenerateTableObject(run_ffn) # Widget
        tabs.addTab(Widget4_bottom, 'Postprocessing')

        ##
        ## Generate tabs
        ##

        layout.addWidget(tabs)
        self.setLayout(layout)


        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()

    ##
