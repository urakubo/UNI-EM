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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
import PyQt5.QtGui as QtGui

from typing import Any


class MiscellaneousSegment():

    def browse_dir_img(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        File = QFileDialog()
        File.List = 1
        newfile = File.getOpenFileName(self.parent, "Select Folder", currentdir, ("Image Files (*.png *.tif *.tiff)"))
        newfile = newfile[0]
        if len(newfile) == 0:
            return False
        newfile = newfile.replace('/', os.sep)
        newdir = os.path.dirname(newfile)
        lineedit_obj.setText(newdir)
        return True


    def browse_dir(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        newdir = QFileDialog.getExistingDirectory(self.parent, "Select Folder", currentdir)
        if len(newdir) == 0:
            return False
        newdir = newdir.replace('/', os.sep)
        lineedit_obj.setText(newdir)
        return True


    def browse_file(self, lineedit_obj):
        currentfile = lineedit_obj.text()
        newfile = QFileDialog.getOpenFileName(self.parent, "Select File", currentfile)
        newfile = newfile[0]
        if len(newfile) == 0:
            return False
        newfile = newfile.replace('/', os.sep)
        lineedit_obj.setText(newfile)
        return True


    def print_current_states(self, obj_args, args, args_title):
        for i, arg in enumerate(args_title):
            if args[i][1] == 'LineEdit':
                param = obj_args[i].text()
                print("{0:>20} : {1:s}".format(arg, param))
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
                print("{0:>20} : {1:d}".format(arg, param))
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
                print("{0:>20} : {1:s}".format(arg, param))
            elif args[i][1] == 'Tab':
                param = obj_args[i].currentIndex()
                print("{0:>20} : {1:s}".format(arg, obj_args[i].tabText(param)))
            elif args[i][1] == 'CheckBox':
                param = obj_args[i].checkState()
                print("{0:>20} : {1:d}".format(arg, param))


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
    def ObtainParams(self, obj_args, args):
        args_header = [args[i][0] for i in range(len(args))]
        params = {}
        for i, arg in enumerate(args):
            param = {}
            if args[i][1] == 'LineEdit':
                param = obj_args[i].text()
            elif args[i][1] == 'SpinBox':
                param = np.str( obj_args[i].value() )
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
            elif args[i][1] == 'Tab':
                id = obj_args[i].currentIndex()
                param = obj_args[i].tabText(id)
            elif args[i][1] == 'CheckBox':
                param = obj_args[i].checkState()
            params[args_header[i]] = param
        return params
    ##
    ##
    def ObtainImageFiles(self, input_path):
        #
        search1 = os.path.join(input_path, '*.png')
        search2 = os.path.join(input_path, '*.tif')
        search3 = os.path.join(input_path, '*.tiff')
        filestack = sorted(glob.glob(search1))
        filestack.extend(sorted(glob.glob(search2)))
        filestack.extend(sorted(glob.glob(search3)))
        return filestack
    ##
    ##
    def ObtainCroppedImage(self, input_image, sx, sy, W,  H, MAXSLIDER):
        #
        imgy, imgx = input_image.shape
        onset_x = (imgx - W) * sx / MAXSLIDER
        onset_y = (imgy - H) * sy / MAXSLIDER
        onset_x = int(onset_x)
        onset_y = int(onset_y)
        onset_x = (onset_x > 0) * onset_x
        onset_y = (onset_y > 0) * onset_y
        output_image = input_image[onset_y: onset_y + H, onset_x: onset_x + W].copy()
        return output_image
    ##
    ##
    def DrawImage(self, input_image, W,  H, canvas):
        qimage1 = QtGui.QImage(input_image, W, H,
                               QtGui.QImage.Format_Grayscale8)
        pixmap1 = QtGui.QPixmap.fromImage(qimage1)
        canvas.setPixmap(pixmap1)
    ##
    ##
    def ObtainNormalizedImage(self, input_image, isChecked):
        if isChecked == True:
            normal_factor = (255 / np.max(input_image)).astype(np.float)
            truth_cropped_normalized = (input_image * normal_factor).astype(np.uint8)
        else:
            truth_cropped_normalized = input_image
        return truth_cropped_normalized
    ##
    ##
    def OrganizeTab2DNN(self, lbl, obj_args, display_order, require_browse_dir, require_browse_dir_img, require_browse_file, Execute):
        tab = QWidget()  # type: Any
        tab.layout = QGridLayout(tab)
        ncol = 8
        browse_button = []
        for i, id in enumerate(display_order):
            tab.layout.addWidget(lbl[id], i + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            tab.layout.addWidget(obj_args[id], i + 1, 1, 1, ncol - 1)
            if id in require_browse_dir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir(obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_img:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir_img(obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda  state, x=id: self.browse_file(obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))



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
        print('2D DNN was not executed.')
        self.parent.close()
        return False

    def SaveParams2D(self):
        self.save_params(self.obj_args, self.args, 'Training')
        return True

    def LoadParams2D(self):
        self.load_params(self.obj_args, self.args, 'Training')
        return True

