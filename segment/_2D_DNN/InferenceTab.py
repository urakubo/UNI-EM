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
import time


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))

from MiscellaneousSegment import MiscellaneousSegment
from ExecuteInference import ExecuteInference

class InferenceTab(MiscellaneousSegment):
    def __init__(self, parent):
        self.parent = parent
        u_info = parent.u_info
        self.tips = [
                        'Path to folder containing images',
                        'Path to folder for storing segmentation',
                        'Directory with checkpoint for training data',
                        'Save Parameters ',
                        'Load Parameters '
                        ]

        datadir   =  u_info.data_path
        imgpath   =  os.path.join(datadir, "_2DNN_test_images")
        outpath   =  os.path.join(datadir, "_2DNN_inference")
        modelpath =  os.path.join(datadir, "_2DNN_model_tensorflow")
        paramfile =  os.path.join(datadir, "parameters", "Inference_2D.pickle")
        self.args = [
                        ['Image Folder',    'LineEdit', imgpath, 'BrowseDirImg'],
                        ['Output Segmentation Folder',   'LineEdit', outpath, 'BrowseDirImg'],
                        ['Checkpoint Folder',      'LineEdit', modelpath, 'BrowseDir'],
                        ['Save Parameters', 'LineEdit',paramfile, 'BrowseFile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'BrowseFile']
                        ]
        self.display_order = [0,1,2,3,4]
        self.args_header   = [self.args[i][0] for i in range(len(self.args))]
        self.obj_args = []

    def Generate(self):

        ## Labels
        lbl   = []
        require_browse_dir = []
        require_browse_dir_img = []
        require_browse_file = []

        ##
        ##
        args = self.args
        for i in range(len(args)):
        ##
            arg = self.args[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(self.SaveParams2D)
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(self.LoadParams2D)
            else :
                lbl.append(QLabel(args[i][0] + ' :'))
                lbl[-1].setToolTip(self.tips[i])

        ##
        for i in range(len(self.args)):
        ##
            if  args[i][1] == 'LineEdit':
                self.obj_args.append( QLineEdit() )
                self.obj_args[-1].setText( self.args[i][2] )
                if self.args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                if self.args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                if self.args[i][3] == 'BrowseFile':
                    require_browse_file.append(i)
            elif args[i][1] == 'SpinBox':
                self.obj_args.append(QSpinBox())
                self.obj_args[-1].setMinimum( args[i][2][0] )
                self.obj_args[-1].setMaximum( args[i][2][2] )
                self.obj_args[-1].setValue( args[i][2][1] )
            elif args[i][1] == 'ComboBox':
                self.obj_args.append(QComboBox())
                items = args[i][2]
                for item in items:
                    self.obj_args[-1].addItem(item)
            else:
                print('Internal error. No fucntion.')

        # Organize tab widget

        tab = self.OrganizeTab2DNN(lbl, self.obj_args, self.display_order, require_browse_dir, require_browse_dir_img, require_browse_file, self._ExecuteInference)
        return tab

    def _ExecuteInference(self):
        ExecuteInference(self.obj_args, self.args)
        QMessageBox.about(self.parent, '2D DNN', 'Inference runs on a different process.')
        return True



