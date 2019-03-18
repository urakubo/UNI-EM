###
###
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, os, time, errno


import numpy as np
import copy
#import shutil
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import subprocess as s
import tornado
import tornado.websocket
import time


from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir          = path.join(main_dir, "icons")
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))
from ExportImgSeg import ExportImgSeg


class ExportImageDialog(QWidget):
    def __init__(self, u_info, parent):
        super().__init__()


        # self.flag = 'images'

        self.left = 200
        self.top = 200
        self.width = 300
        self.height = 150
        self.comboText = None
        self.u_info = u_info
        self.parent = parent

        self.flag   = 'images'
        self.title  = "Export Images"
        self.choice = ["PNG, 16bit, Grayscale", "PNG, 8bit, Grayscale",
                  "TIFF, 16bit, Grayscale", "TIFF, 8bit, Grayscale",
                  "Multi-TIFF, 16bit, Grayscale", "Multi-TIFF, 8bit, Grayscale",
                  "NUMPY, 32bit, uint (npy)", "NUMPY, 32bit, uint (npz), 'stack'", "HDF, 64bit, int, 'stack'"]
        self.table = ["PNG16G", "PNG8G",
                      "TIF16G", "TIF8G",
                      "MTIF16G", "MTIF8G",
                      "NUMPY32", "NUMPY32C", "HDF64"]
        self.initUI()

    def initUI(self):

        # Labels
        lbl1 = QLabel('Format:')
        lbl2 = QLabel('Filename:')
        lbl3 = QLabel('Start At:')
        lbl4 = QLabel('Digits(1-8):')


        # Input box
        self.edit1_fmat = QComboBox(self)
        for ch in self.choice:
            self.edit1_fmat.addItem(ch)
        self.comboText = self.choice[0]
        self.edit1_fmat.activated[str].connect(self.onActivated)

        self.edit2_fname = QLineEdit()
        self.edit3_start = QSpinBox()
        self.edit3_start.setMinimum(0)
        self.edit4_digit = QSpinBox()
        self.edit4_digit.setRange(1, 8)
        self.edit4_digit.setValue(4)

        # Button
        ok_import = QPushButton("OK")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(self._ExecuteExport)
        cl_import.clicked.connect(self._Cancel)


        layout = QGridLayout()
        layout.addWidget(lbl1, 0, 0, alignment=(Qt.AlignRight))
        layout.addWidget(lbl2, 1, 0, alignment=(Qt.AlignRight))
        layout.addWidget(lbl3, 2, 0, alignment=(Qt.AlignRight))
        layout.addWidget(lbl4, 3, 0, alignment=(Qt.AlignRight))

        layout.addWidget(self.edit1_fmat, 0, 1, 1, 2)
        layout.addWidget(self.edit2_fname, 1, 1, 1, 2)
        layout.addWidget(self.edit3_start, 2, 1, 1, 2)
        layout.addWidget(self.edit4_digit, 3, 1, 1, 2)
        # addWidget(*Widget, row, column, rowspan, colspan)

        layout.addWidget(ok_import, 4, 1, alignment=(Qt.AlignRight))
        layout.addWidget(cl_import, 4, 2)

        self.setLayout(layout)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()

    def onActivated(self, text):
        self.comboText = text

    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False

    def _ExecuteExport(self):  # wxGlade: ImportImagesSegments.<event_handler>
        #
        # Dialog to specify directory
        #
        dir = QFileDialog.getExistingDirectory(self, "Select Export Folder", self.u_info.files_path)
        if len(dir) == 0:
            print('Failed to open directory!')
            return
        #
        #


        ftype_id = self.choice.index(self.comboText)


        ftype     = self.table[ftype_id]
        fname     = self.edit2_fname.text()
        startid   = self.edit3_start.value()
        numdigit  = self.edit4_digit.value()

        print(self.flag)
        print('Filedir:    ', dir)
        print('Filename:   ', fname )
        print('Filetype:   ', ftype )
        print('Init ID:    ', startid )
        print('Num Digits: ', numdigit )

        exports = ExportImgSeg()
        exports.run(self.u_info, dir, fname, ftype, startid, numdigit, self.flag)

        self.close()
        return True

