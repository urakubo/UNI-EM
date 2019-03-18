import sys, os, time, errno


import numpy as np
import copy
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import tornado
import tornado.websocket
import glob     # Wild card
import cv2
import threading

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, QSlider, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, \
    QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSlot


import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "segment"))
from MiscellaneousSegment import MiscellaneousSegment
from Executor  import Executor

H = 256
W = 256
MAXSLIDER = 100

class ThumbnailGeneratorFFN(MiscellaneousSegment):

    def __init__(self, parent):
        self.parent = parent

    def GenerateThumbnailObject(self, filter, obj_args, args):

        ##
        ## Canvas
        ##
        self.training_image_cropped = []
        self.truth_image_cropped = []
        self.filter = filter
        self.obj_args = obj_args
        self.args = args

        def _ChangeZ():
            params = self.ObtainParams(self.obj_args, self.args)
            self.training_file_stack = self.ObtainImageFiles(params['Training Image Folder'])
            self.ground_truth_file_stack = self.ObtainImageFiles(params['Ground Truth Folder'])
            sz = self.control_thumbnail[0].value()  # Z 0:99
            if len(self.training_file_stack) > 0 and len(self.ground_truth_file_stack) > 0:
                znum = len(self.training_file_stack)
                id = np.floor(znum * sz / MAXSLIDER).astype(np.uint16)
                self.training_image = cv2.imread(self.training_file_stack[id], cv2.IMREAD_GRAYSCALE)
                znum = len(self.ground_truth_file_stack)
                id = np.floor(znum * sz / MAXSLIDER).astype(np.uint16)
                self.ground_truth = cv2.imread(self.ground_truth_file_stack[id], -1).astype(np.uint8)
                _ChangeXY()


        def _ChangeXY():
            sx = self.control_thumbnail[1].value()  # X 0:99
            sy = self.control_thumbnail[2].value()  # y 0:99

            if len(self.training_image) > 0 and len(self.ground_truth) > 0:

                self.training_image_cropped = self.ObtainCroppedImage(self.training_image, sx, sy, W, H, MAXSLIDER)
                training_cropped_normalized = self.ObtainNormalizedImage(self.training_image_cropped, self.normal_training_image.isChecked())
                self.DrawImage(training_cropped_normalized, W, H, self.canvas1)

                self.ground_truth_cropped = self.ObtainCroppedImage(self.ground_truth, sx, sy, W, H, MAXSLIDER)
                truth_cropped_normalized = self.ObtainNormalizedImage(self.ground_truth_cropped, self.normal_ground_truth.isChecked())
                self.DrawImage(truth_cropped_normalized, W, H, self.canvas2)

        ##
        ##
        ##

        image1 = (np.ones((H, W))*128).astype(np.uint8)
        self.canvas1 = QLabel()
        self.canvas2 = QLabel()

        self.DrawImage(image1.data, W, H, self.canvas1)
        self.DrawImage(image1.data, W, H, self.canvas2)

        slider_names    = ['Target Z', 'Target X', 'Target Y']
        slider_events   = [ _ChangeZ, _ChangeXY, _ChangeXY ]

        self.control_thumbnail  = []
        s = []
        vbox = QVBoxLayout()
        for i in range(len(slider_names)) :
            vbox.addWidget(QLabel(slider_names[i]))
            s.append(QSlider(Qt.Horizontal))
            s[-1].setFocusPolicy(QtCore.Qt.NoFocus)
            s[-1].setTickPosition(QSlider.TicksBothSides)
            s[-1].setMinimum(0)
            s[-1].setMaximum(MAXSLIDER-1)
            s[-1].setValue(0)
            s[-1].setTickInterval(20)
            s[-1].setSingleStep(1)
            vbox.addWidget(s[-1])
            s[-1].valueChanged.connect(slider_events[i])
            self.control_thumbnail.append(s[-1])
        ##
        ##
        self.normal_training_image = QCheckBox('Training image normalized')
        self.normal_training_image.move(20, 20)
        self.normal_training_image.stateChanged.connect( _ChangeZ )
        vbox.addWidget(self.normal_training_image)
        self.normal_ground_truth = QCheckBox('Ground truth normalized')
        self.normal_ground_truth.move(20, 20)
        self.normal_ground_truth.stateChanged.connect( _ChangeZ )
        vbox.addWidget(self.normal_ground_truth)
        ##
        ##

        ### Initial sample image
        _ChangeZ()

        ### Generate objects
        thumb = QWidget()
        thumb.layout = QGridLayout(thumb)

        thumb.layout.addWidget(QLabel('Training image'), 0, 0, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(QLabel('Ground truth'), 0, 1, alignment=Qt.AlignCenter)

        thumb.layout.addWidget(self.canvas1, 1, 0, 1, 1, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(self.canvas2, 1, 1, 1, 1, alignment=Qt.AlignCenter)

        thumb.layout.addLayout(vbox, 0, 2, -1, 1, alignment=Qt.AlignCenter)

        thumb.layout.setRowStretch(3, 2) # I do not understand why >(5, 1) produces top aligned rows.
        thumb.setLayout(thumb.layout)

        return thumb
