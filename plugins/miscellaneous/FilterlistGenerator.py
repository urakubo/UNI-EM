import sys, os, time, errno

import numpy as np
import copy

from miscellaneous.ListManager import ListManager
from Filter2D3D.FiltersInfo import FilterInfo

from PyQt5.QtWidgets import  QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSlot, QStringListModel, QEvent


import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
from miscellaneous.MiscellaneousFilters  import MiscellaneousFilters


class FilterlistGenerator(MiscellaneousFilters):

    def _title(self, text):
        bold = QFont()
        bold.setBold(True)
        ql = QLabel(text)
        ql.setFont(bold)
        ql.setAlignment(Qt.AlignTop)
        ql.setMaximumHeight(20)
        return ql

    def __init__(self, parent):
        self.parent = parent


    def GenerateFilterlistObject(self):
        ##
        ##
        fi = FilterInfo()
        _2D_Filters = fi.get_2d_filter_name_list()
        _3D_Filters = fi.get_3d_filter_name_list()

        ##
        ## Canvas
        ##
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout2_1 = QVBoxLayout()
        layout2_2 = QVBoxLayout()
        self.listManager = ListManager(self)
        ##
        layout1.addWidget(self._title("2D Filter"))
        self.listManager.addSource(layout1, _2D_Filters)
        ##
        layout1.addWidget(self._title("3D Filter"))
        self.listManager.addSource(layout1, _3D_Filters)
        ##
        layout2_1.addWidget(self._title("Filter Application"), alignment=Qt.AlignTop)
        self.listManager.addTarget(layout2_1)
        layout2_1.setAlignment(Qt.AlignTop)
        ##
        self.listManager.addParameter(layout2_1)
        ##
        b = QPushButton("Obtain sample output")
        b.clicked.connect(self.parent.obtainSample)
        layout2_2.addWidget(b, alignment=Qt.AlignBottom)

        layout2.addLayout(layout2_1)
        layout2.addLayout(layout2_2)

        self.parent.targetWidget = self.listManager.widgets[2]

        ##
        layout = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        ### Generate objects
        filterlist = QWidget()
        filterlist.setLayout(layout)

        return filterlist

