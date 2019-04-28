import sys, os, time, errno, math


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
    QLabel, QCheckBox, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSlot


import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
from miscellaneous.MiscellaneousFilters  import MiscellaneousFilters
from miscellaneous.CanvasLabel import CanvasLabel
from Filters.FiltersInfo import FiltersInfo


import miscellaneous.Miscellaneous as m

H = 300 # 384
W = 300 # 384
MAXSLIDER = 100

class ThumbnailGenerator(MiscellaneousFilters):

    def _title(self, text):
        bold = QFont()
        bold.setBold(True)
        ql = QLabel(text)
        ql.setFont(bold)
        return ql

    def __init__(self, parent):
        self.parent = parent

        self.currentX = 0
        self.currentY = 0

        self.fi = FiltersInfo()


    def GenerateThumbnailObject(self, obj_args, args):
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
            if len(self.control_thumbnail) > 1:
                sx = self.control_thumbnail[1].value()  # X 0:99
                sy = self.control_thumbnail[2].value()  # y 0:99
            else:
                sx = 0
                sy = 0
            _ChangeXYImpl(sx, sy)
        def _ChangeXYImpl(sx, sy):
            self.currentX += sx
            self.currentY += sy
            
            if len(self.target_image) > 0:
                imgy, imgx = self.target_image.shape

                onset_x = self.currentX
                onset_y = self.currentY

                if onset_x < 0:
                    onset_x = 0
                if onset_y < 0:
                    onset_y = 0

                if onset_x > (imgx - W):
                    onset_x = imgx - W
                if onset_y > (imgy - H):
                    onset_y = imgy - H

                self.currentX = onset_x
                self.currentY = onset_y

                self.image_cropped = np.zeros((H, W), dtype=np.uint8)
                self.image_cropped = self.target_image[onset_y: onset_y + H, onset_x: onset_x + W].copy()

                if self.norm_sample.isChecked() == True:
                    normal_factor = (255 / np.max(self.image_cropped)).astype(np.float)
                    cropped_normalized = (self.image_cropped * normal_factor).astype(np.uint8)
                else:
                    cropped_normalized = self.image_cropped

                qimage1 = QtGui.QImage(cropped_normalized, W, H, QtGui.QImage.Format_Grayscale8)
                pixmap1 = QtGui.QPixmap.fromImage(qimage1)
                self.canvas1.setPixmap(pixmap1)

        def Execute():
            self.filestack = self.ObtainTarget()
            if self.filestack == [] :
                return False
            w = self.parent.targetWidget
            if w.count() == 0:
                print('No filter.')
                return False
            ##
            ## Filter check (2d/3d)
            ##
            types = []
            for i in range(w.count()):
                item = w.item(i)
                text = item.text()
                type = self.fi.get_type(text)
                types.append(type)
            # print(types)
            if '3d' in types :
                self.Execute3D(w)
            else:
                self.Execute2D(w)



        def Cancel():  # wxGlade: ImportImagesSegments.<event_handler>
            self.parent.close()
            print('Filter was not applied.')
            return False

        def _ObtainSample():
            self.filestack = self.ObtainTarget()
            if self.filestack == [] :
                return False
            w = self.parent.targetWidget
            if w.count() == 0:
                print('No filter.')
                return False
            print('Calculate sample output image')

            ## Filter application
            _ChangeZ()
            cropped_image_for_filter = self.FilterApplication2D(w, self.image_cropped)

            ## Display sample output image
            cropped_image = cropped_image_for_filter.astype(np.uint8)
            if self.norm_output.isChecked() == True and np.max(cropped_image) > 1:
                normal_factor = (255 / np.max(cropped_image)).astype(np.float)
                cropped_image = (cropped_image * normal_factor).astype(np.uint8)

            qimage2 = QtGui.QImage(cropped_image.data, W, H, QtGui.QImage.Format_Grayscale8)
            pixmap2 = QtGui.QPixmap.fromImage(qimage2)
            self.canvas2.setPixmap(pixmap2)

        ##
        ## Canvas
        ##
        self.target_image  = []
        self.image_cropped = []
        # self.filter   = filter
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

        self.canvas1 = CanvasLabel()
        self.canvas1.setPixmap(pixmap1)
        self.canvas1.changePosCallback = _ChangeXYImpl

        self.canvas2 = CanvasLabel()
        self.canvas2.setPixmap(pixmap2)

        slider_names    = ['Target Z']
        slider_events   = [ _ChangeZ ]

        self.control_thumbnail  = []
        targetz_label = QLabel('Target Z')

        s = QSlider(Qt.Horizontal)
        s.setFocusPolicy(QtCore.Qt.NoFocus)
        s.setTickPosition(QSlider.TicksBothSides)
        s.setMinimum(0)
        s.setMaximum(MAXSLIDER-1)
        s.setValue(0)
        s.setTickInterval(20)
        s.setSingleStep(1)
        s.setFixedWidth(200)
        s.valueChanged.connect(_ChangeZ)

        self.control_thumbnail.append(s)
        ##
        ##
        self.norm_sample = QCheckBox('normalized')
        self.norm_sample.move(20, 20)
        self.norm_sample.stateChanged.connect(_ChangeXY)
        ##
        ##
        self.norm_output = QCheckBox('normalized')
        self.norm_output.move(20, 20)
        self.norm_output.stateChanged.connect( _ObtainSample )
        ##
        ##
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setMinimumWidth(130)
        cl_import.setMinimumWidth(130)
        ok_import.clicked.connect(Execute)
        cl_import.clicked.connect(Cancel)

        self.parent.obtainSample = _ObtainSample

        ### Initial sample image
        _ChangeZ()

        ### Generate objects
        thumb = QWidget()
        thumb.layout = QGridLayout(thumb)

        thumb.layout.addWidget(self._title('Target image'), 0, 1, 1, 3, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(self._title('Sample output image'), 0, 4, 1, 3, alignment=Qt.AlignCenter)

        thumb.layout.addWidget(self.canvas1, 1, 1, 1, 3, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(self.norm_sample, 2, 3, 1, 1, alignment=Qt.AlignRight)
        thumb.layout.addWidget(targetz_label, 3, 1, 1, 1, alignment=Qt.AlignLeft)
        thumb.layout.addWidget(s, 3, 2, 1, 1, alignment=Qt.AlignLeft)

        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.addWidget(ok_import)
        btn_layout.addWidget(cl_import)
        btn_frame.setStyleSheet('QFrame {border: 1px solid gray;border-radius:8px;padding: 0px;margin: 0px}')
        thumb.layout.addWidget(btn_frame, 3, 6, 1, 1)

        thumb.layout.addWidget(self.canvas2, 1, 4, 1, 3, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(self.norm_output, 2, 6, 1, 1, alignment=Qt.AlignRight)

        thumb.layout.setRowStretch(3, 2) # I do not understand why >(5, 1) produces top aligned rows.
        thumb.setLayout(thumb.layout)

        return thumb
