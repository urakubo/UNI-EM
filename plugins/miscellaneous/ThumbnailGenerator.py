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
from MiscellaneousPlugins  import MiscellaneousPlugins
from Executor  import Executor

H = 256
W = 256
MAXSLIDER = 100

class ThumbnailGenerator(MiscellaneousPlugins):

    def __init__(self, parent):
        self.parent = parent


    def GenerateThumbnailObject(self, filter, obj_args, args):
        ##
        ##
        ##

        def _ChangeZ():
            self.filestack = self.ObtainTarget()
            sz = self.control_thumbnail[0].value()  # Z 0:99
            if len(self.filestack) > 0:
                znum = len(self.filestack)
                id = np.floor(znum * sz / MAXSLIDER).astype(np.uint16)
                self.target_image = cv2.imread(self.filestack[id], cv2.IMREAD_GRAYSCALE).astype(np.uint8)
                _ChangeXY()

        def _ChangeXY():
            sx = self.control_thumbnail[1].value()  # X 0:99
            sy = self.control_thumbnail[2].value()  # y 0:99

            if len(self.target_image) > 0:
                imgy, imgx = self.target_image.shape

                onset_x = (imgx - W) * sx / MAXSLIDER
                onset_y = (imgy - H) * sy / MAXSLIDER
                onset_x = int(onset_x)
                onset_y = int(onset_y)

                onset_x = (onset_x > 0) * onset_x
                onset_y = (onset_y > 0) * onset_y
                self.image_cropped = np.zeros((H, W), dtype=np.uint8)
                self.image_cropped = self.target_image[onset_y: onset_y + H, onset_x: onset_x + W].copy()

                if self.norm_sample.isChecked() == True:
                    normal_factor = (255 / np.max(self.image_cropped)).astype(np.float)
                    cropped_normalized = (self.image_cropped * normal_factor).astype(np.uint8)
                else:
                    cropped_normalized = self.image_cropped

                qimage1 = QtGui.QImage(cropped_normalized, W, H,
                                       QtGui.QImage.Format_Grayscale8)
                pixmap1 = QtGui.QPixmap.fromImage(qimage1)
                self.canvas1.setPixmap(pixmap1)

        def _ObtainSample():
            if len(self.image_cropped) > 0:
                _ChangeZ()
                params = self.ObtainParams(self.obj_args, self.args)
                output_image = self.filter.Filter(self.image_cropped, params)
                output_image = output_image.astype(np.uint8)

                if self.norm_output.isChecked() == True:
                    normal_factor = (255 / np.max(output_image)).astype(np.float)
                    cropped_normalized = (output_image * normal_factor).astype(np.uint8)
                else:
                    cropped_normalized = output_image

                qimage2 = QtGui.QImage(cropped_normalized.data, W, H,
                                       QtGui.QImage.Format_Grayscale8)
                pixmap2 = QtGui.QPixmap.fromImage(qimage2)
                self.canvas2.setPixmap(pixmap2)

        ##
        ## Canvas
        ##
        self.target_image  = []
        self.image_cropped = []
        self.filter   = filter
        self.obj_args = obj_args
        self.args     = args

        image1 = (np.ones((H, W))*128).astype(np.uint8)
        image2 = (np.ones((H, W))*128).astype(np.uint8)

        qimage1 = QtGui.QImage(image1.data, image1.shape[1], image1.shape[0],
                              QtGui.QImage.Format_Grayscale8)
        pixmap1 = QtGui.QPixmap.fromImage(qimage1)

        qimage2 = QtGui.QImage(image2.data, image2.shape[1], image2.shape[0],
                              QtGui.QImage.Format_Grayscale8)
        pixmap2 = QtGui.QPixmap.fromImage(qimage2)

        self.canvas1 = QLabel()
        self.canvas1.setPixmap(pixmap1)

        self.canvas2 = QLabel()
        self.canvas2.setPixmap(pixmap2)


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
        self.norm_sample = QCheckBox('Target normalized')
        self.norm_sample.move(20, 20)
        self.norm_sample.stateChanged.connect(_ChangeXY)
        vbox.addWidget(self.norm_sample)
        self.norm_output = QCheckBox('Output normalized')
        self.norm_output.move(20, 20)
        self.norm_output.stateChanged.connect( _ObtainSample )
        vbox.addWidget(self.norm_output)
        ##
        ##
        ##
        b = QPushButton("Obtain sample output")
        b.clicked.connect( _ObtainSample )
        vbox.addWidget(b)

        ### Initial sample image
        _ChangeZ()


        ### Generate objects
        thumb = QWidget()
        thumb.layout = QGridLayout(thumb)

        thumb.layout.addWidget(QLabel('Target image'), 0, 0, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(QLabel('Output image'), 0, 1, alignment=Qt.AlignCenter)

        thumb.layout.addWidget(self.canvas1, 1, 0, 1, 1, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(self.canvas2, 1, 1, 1, 1, alignment=Qt.AlignCenter)

        thumb.layout.addLayout(vbox, 0, 2, -1, 1, alignment=Qt.AlignCenter)

        thumb.layout.setRowStretch(3, 2) # I do not understand why >(5, 1) produces top aligned rows.
        thumb.setLayout(thumb.layout)

        return thumb
