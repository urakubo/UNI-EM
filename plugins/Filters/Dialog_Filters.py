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

import miscellaneous.Miscellaneous as m
from miscellaneous.SyncListQComboBoxManager import *
from miscellaneous.MiscellaneousFilters  import MiscellaneousFilters
from miscellaneous.ThumbnailGenerator    import ThumbnailGenerator
from miscellaneous.FilterlistGenerator   import FilterlistGenerator

from Filters.filters.Gaussian import Gaussian
from Filters.filters.Binary   import Binary
from Filters.filters.Invert   import Invert
from Filters.filters.Label   import Label
from Filters.filters.Canny   import Canny
from Filters.filters.Skimg   import Skimg
from Filters.filters.CLAHE   import CLAHE

class Dialog_Filters(QWidget, MiscellaneousFilters):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 900
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "2D/3D Filters"
        self.initUI()

    def initUI(self):
        ###
        ### bottom
        ###

        table1 = TableGenerator(self)
        widget_bottom, obj_args, args = table1.GenerateTableObject()  # Widget

        ###
        ### Top
        ###

        thumb1 = ThumbnailGenerator(self)
        widget_top_right = thumb1.GenerateThumbnailObject(obj_args, args)  # Widget

        self.filter_list = FilterlistGenerator(self)
        widget_top_left  = self.filter_list.GenerateFilterlistObject()  # Widget


        self.targ_image_folder_qcombo.activated.connect( self.ChangeZ )
        # self.targ_image_folder_qcomboは
        # サムネイル画像アップデート用。同コンボボックスの変更に併せて呼び出されるようにしたいが、
        # 上手く動かない。

        widget_top = QWidget()
        widget_top.layout = QHBoxLayout(widget_top)
        widget_top.layout.addWidget(widget_top_left)
        widget_top.layout.addWidget(widget_top_right)

        ###
        ### Connect bottom top
        ###
        widget_all = QWidget()
        widget_all.layout = QVBoxLayout(widget_all)
        widget_all.layout.addWidget(widget_top)
        widget_all.layout.addWidget(widget_bottom)
        self.setLayout(widget_all.layout)

        ##
        ## Generate tabs
        ##

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()


class TableGenerator(MiscellaneousFilters):

    def __init__(self, parent):
        self.parent = parent


    def GenerateTableObject(self):

        paramfile = os.path.join(self.parent.u_info.parameters_path, "Filters.pickle")

        args = [
                        'Target Folder',
                        'Output Folder',
                        'Save Parameters',
                        'Load Parameters',
                    ]
        lbl      = []
        obj_args = []

        lbl.append(QLabel('Target Folder:'))
        lbl[-1].setToolTip('Path to folder containing images')
        self.parent.targ_image_folder_qcombo = SyncListQComboBoxExcludeDjojMtifManager.get().create(self, 1)
        obj_args.append( self.parent.targ_image_folder_qcombo )

        lbl.append(QLabel('Output Folder:'))
        lbl[-1].setToolTip('Path to folder containing images')
        obj_args.append( SyncListQComboBoxExcludeDjojMtifManager.get().create(self, 2) )

        lbl.append(QPushButton('Save Parameters'))
        lbl[-1].clicked.connect(lambda: self.save_params(args, obj_args))
        obj_args.append(QLineEdit())
        obj_args[-1].setText(paramfile)

        lbl.append(QPushButton('Load Parameters'))
        lbl[-1].clicked.connect(lambda: self.load_params(args, obj_args))
        obj_args.append(QLineEdit())
        obj_args[-1].setText(paramfile)

        table = QWidget()
        table.layout = QGridLayout(table)
        ncol = 8
        browse_button = []
        for id in range(len(args)):
            table.layout.addWidget(lbl[id], id + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            table.layout.addWidget(obj_args[id], id + 1, 1, 1, ncol - 1)

            if id in [0,1]: # require_browse_open_img
                browse_button.append(QPushButton("Open..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_OpenImageFolder(obj_args[z]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))

            elif id in [2,3] : # 'Browsefile'
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_file(obj_args[x]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))


        return table, obj_args, args

