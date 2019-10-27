import sys, os, time, errno, math


import numpy as np
import pickle
import glob


from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, pyqtSlot


from miscellaneous.MiscellaneousFilters import MiscellaneousFilters
from miscellaneous.SyncListQComboBoxManager import *


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
        self.parent.targ_image_folder_qcombo = SyncListQComboBoxExcludeDojoMtifManager.get().create(self, 1)
        obj_args.append( self.parent.targ_image_folder_qcombo )

        lbl.append(QLabel('Output Folder:'))
        lbl[-1].setToolTip('Path to folder containing images')
        obj_args.append( SyncListQComboBoxExcludeDojoMtifManager.get().create(self, 2) )

        lbl.append(QPushButton('Save Parameters'))
        lbl[-1].clicked.connect(lambda: self.SaveParamsFilter(args, obj_args))
        obj_args.append(QLineEdit())
        obj_args[-1].setText(paramfile)

        lbl.append(QPushButton('Load Parameters'))
        lbl[-1].clicked.connect(lambda: self.LoadParamsFilter(args, obj_args))
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

