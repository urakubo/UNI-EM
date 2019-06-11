##
##
##
import sys, os, time, errno
import h5py
import cv2
import png
from itertools import product
import glob

import numpy as np
import copy
import pickle


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, QCheckBox, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, \
    QTreeView, QFileSystemModel, QListView, QTableView, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot,  QAbstractListModel, QModelIndex, QVariant, QDir, QSize
import PyQt5.QtGui as QtGui

from typing import Any

import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)

from miscellaneous.SharedFileDialogs import SharedFileDialogs
import miscellaneous.Miscellaneous as m

class MiscellaneousSegment(SharedFileDialogs):

    def save_params(self, obj_args, args, filter_name):
        #
        args_header = [args[i][0] for i in range(len(args))]
        id = args_header.index('Save Parameters')
        filename = obj_args[id].text()
        params = self.ObtainParams(obj_args, args)

        print('')
        print('Save file : ', filename)
        self.print_current_states(obj_args, args, args_header)
        print('')
        try:
            with open(filename, mode='wb') as f:
                pickle.dump(params, f)
            print(filter_name, ': Parameter file was saved.')
        except:
            print(filter_name, ': Parameter file could not be saved.')
            return False

        return True
    ##
    ##
    def load_params(self, obj_args, args, filter_name):
        #
        args_header = [args[i][0] for i in range(len(args))]
        id = args_header.index('Load Parameters')
        filename = obj_args[id].text()
        print('')
        print('Load file : ', filename)
        try:
            with open(filename, mode='rb') as f:
                params = pickle.load(f)
        except:  # parent of IOError, OSError *and* WindowsError where available
            print(filter_name, ': Parameter file cannot be open.')
            return False

        for i, arg in enumerate(args_header):
            if args[i][1] == 'LineEdit':
                obj_args[i].setText(params[args_header[i]])
            elif args[i][1] == 'SpinBox':
                print(params[args_header[i]])
                obj_args[i].setValue(int(params[args_header[i]]))
            elif args[i][1] == 'ComboBox':
                id = obj_args[i].findText(params[args_header[i]])
                obj_args[i].setCurrentIndex(id)
            elif args[i][1] == 'Tab':
                obj_args[i].setCurrentIndex(  args[i][2].index(params[args_header[i]])  )
            elif args[i][1] == 'CheckBox':
                obj_args[i].setCheckState(params[args_header[i]])

        self.print_current_states(obj_args, args, args_header)
        return True
    ##
    ##

    def OrganizeTab2DNN(self, require_browse_dir, require_browse_dir_img,
                        require_browse_file, require_browse_open_img, Execute):
        tab = QWidget()  # type: Any
        tab.layout = QGridLayout(tab)
        ncol = 8
        browse_button = []
        for i, id in enumerate(self.display_order):
            tab.layout.addWidget(self.lbl[id], i + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            tab.layout.addWidget(self.obj_args[id], i + 1, 1, 1, ncol - 1)
            if id in require_browse_dir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir(self.obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_img:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir_img(self.obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda  state, x=id: self.browse_file(self.obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_open_img:
                browse_button.append(QPushButton("Open..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_OpenImageFolder(self.obj_args[z]))
                tab.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))


        ## Execute & cancel buttons
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(Execute)
        cl_import.clicked.connect(self.Cancel2D)
        tab.layout.addWidget(ok_import, i + 2, 1, alignment=(Qt.AlignRight))
        tab.layout.addWidget(cl_import, i + 2, 2)
        tab.layout.setRowStretch(10, 1) # I do not understand why >(5, 1) produces top aligned rows.
        tab.setLayout(tab.layout)

        return tab


    def Cancel2D(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.parent.close()
        return False

    def SaveParams2D(self):
        self.save_params(self.obj_args, self.args, 'Training')
        return True

    def LoadParams2D(self):
        self.load_params(self.obj_args, self.args, 'Training')
        return True

