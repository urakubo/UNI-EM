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
from _2D_DNN.MiscellaneousSegment import MiscellaneousSegment
from _2D_DNN.ExecuteTraining import ExecuteTraining
from miscellaneous.SyncListQComboBoxManager import *

class TrainingTab(MiscellaneousSegment):
    def __init__(self, parent):
        self.parent = parent
        u_info = parent.u_info
        self.tips = [
                        'Path to folder containing images',
                        'Path to folder containing segmentation',
                        'Directory with checkpoint to resume training from or use for testing',
                        'Number of images in batch',
                        'Loss Function',
                        'Number of training epochs',
                        'Write current training images every display frequency steps',
                        'Dimensions for Augmentation',
                        'Save Parameters ',
                        'Load Parameters ',
                        'Depth of U-net (maximum 8)',
                        'Number of residual blocks in res net',
                        'Number of highway units in highway net',
                        'Number of dense blocks in dense net',
                        'Number of dense connected layers in each block of the dense net',
                        'Network topology'
                        ]

        modelpath =  u_info.tensorflow_model_path
        paramfile = os.path.join( u_info.parameters_path, "Training_2D.pickle")
        self.args = [
                        ['Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Segmentation Folder',   'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder',      'LineEdit', modelpath, 'BrowseDir'],
                        ['Batch Size', 'SpinBox', [1, 1, 65535]],
                        ['Loss Function', 'ComboBox', ["softmax", "hinge", "square", "approx", "dice", "logistic"]],
                        ['Maximal Epochs', 'SpinBox', [1, 2000, 65535]],
                        ['Display Frequency', 'SpinBox', [0, 200, 65535]],
                        ['Augmentation',    'ComboBox', ["fliplr, flipud, transpose", "fliplr, flipud", "fliplr", "flipud", "None"]],
                        ['Save Parameters', 'LineEdit',paramfile, 'BrowseFile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'BrowseFile'],
                        ['U depth','SpinBox',[1,8,20]],
                        ['N res blocks','SpinBox',[1,9,255]],
                        ['N highway units','SpinBox',[1,9,255]],
                        ['N dense blocks','SpinBox',[1,5,255]],
                        ['N dense layers','SpinBox',[1,5,255]],
                        ['Network', 'Tab', ['unet', 'resnet', 'highwaynet', 'densenet']]
                        ]

        #                         'Model',
        #  ['Model', 'ComboBox',   ['pix2pix','pix2pix2','CycleGAN']]

        self.display_order = [0, 1, 2, -1, 3, 4, 5, 6, 7, 8, 9]
        self.args_header   = [self.args[i][0] for i in range(len(self.args))]
        self.obj_args = []

    def Generate(self):

        ## Labels
        self.lbl   = []
        require_browse_dir = []
        require_browse_dir_img = []
        require_browse_file = []
        require_browse_open_img = []
        ##
        for i in range(len(self.args)):
        ##
            arg = self.args[i][0]
            if arg == 'Save Parameters':
                self.lbl.append(QPushButton(arg))
                self.lbl[-1].clicked.connect(self.SaveParams2D)
            elif arg == 'Load Parameters':
                self.lbl.append(QPushButton(arg))
                self.lbl[-1].clicked.connect(self.LoadParams2D)
            else :
                self.lbl.append(QLabel(self.args[i][0] + ' :'))
                self.lbl[-1].setToolTip(self.tips[i])
        ##
        for i in range(len(self.args)):
        ##
            if  self.args[i][1] == 'LineEdit':
                self.obj_args.append( QLineEdit() )
                self.obj_args[-1].setText( self.args[i][2] )
                if self.args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                if self.args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                if self.args[i][3] == 'BrowseFile':
                    require_browse_file.append(i)
            elif self.args[i][1] == 'SpinBox':
                self.obj_args.append(QSpinBox())
                self.obj_args[-1].setMinimum( self.args[i][2][0] )
                self.obj_args[-1].setMaximum( self.args[i][2][2] )
                self.obj_args[-1].setValue( self.args[i][2][1] )
            elif self.args[i][1] == 'ComboBox':
                self.obj_args.append(QComboBox())
                items = self.args[i][2]
                for item in items:
                    self.obj_args[-1].addItem(item)
            elif self.args[i][1] == 'Tab':
                # Add tabs
                self.obj_args.append(QTabWidget())
                ttab = []
                for ttab_title in self.args[i][2]:
                    ttab.append( QWidget() )
                    self.obj_args[-1].addTab(ttab[-1], ttab_title)
                self._Training2D_Unet(ttab[0], self.lbl)
                self._Training2D_Resnet(ttab[1], self.lbl)
                self._Training2D_Highwaynet(ttab[2], self.lbl)
                self._Training2D_Densenet(ttab[3], self.lbl)
            elif self.args[i][1] == 'SelectImageFolder':
                self.obj_args.append(SyncListQComboBoxExcludeDjojMtifManager.get().create(self, i))
                #for item in self.parent.u_info.open_files:
                #    if self.parent.u_info.open_files_type[item] != 'Dojo':
                #       self.obj_args[-1].addItem(item)
                if self.args[i][2] == 'OpenImageFolder':
                    require_browse_open_img.append(i)
            else:
                print('Internal error. No fucntion.')

        # Organize tab widget
        tab = self.OrganizeTab2DNN(require_browse_dir, require_browse_dir_img,
                                   require_browse_file, require_browse_open_img,  self._ExecuteTraining)
        return tab

    def _Training2D_Unet(self, ttab, lbl):
        id = self.args_header.index('U depth')
        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args[id], 1, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _Training2D_Resnet(self, ttab, lbl):
        id = self.args_header.index('N res blocks')
        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args[id], 1, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _Training2D_Highwaynet(self, ttab, lbl):
        id = self.args_header.index('N highway units')
        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args[id], 1, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _Training2D_Densenet(self, ttab, lbl):
        id1 = self.args_header.index('N dense blocks')
        id2 = self.args_header.index('N dense layers')

        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id1], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args[id1], 1, 1, 1, 4)
        ttab.layout.addWidget(lbl[id2], 2, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args[id2], 2, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _ExecuteTraining(self):
        ExecuteTraining(self.obj_args, self.args, self.parent)
        QMessageBox.about(self.parent, '2D DNN', 'Training runs on a different process.\nLaunch Tensorboard to monitor the progress.')
        return True
