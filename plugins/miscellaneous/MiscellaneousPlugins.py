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


class MiscellaneousPlugins():
    ##




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
            if   args[i][1] == 'LineEdit':
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
        except :
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
        except :  # parent of IOError, OSError *and* WindowsError where available
            print(filter_name, ': Parameter file cannot be open.')
            return False

        for i, arg in enumerate(args_header):
            if   args[i][1] == 'LineEdit':
                obj_args[i].setText( params[args_header[i]] )
            elif args[i][1] == 'SpinBox':
                obj_args[i].setValue( params[args_header[i]] )
            elif args[i][1] == 'ComboBox':
                id = obj_args[i].findText( params[args_header[i]] )
                obj_args[i].setCurrentIndex( id )
            elif args[i][1] == 'Tab':
                obj_args[i].setCurrentIndex( params[args_header[i]] )
            elif args[i][1] == 'CheckBox':
                obj_args[i].setCheckState( params[args_header[i]] )

        self.print_current_states(obj_args, args, args_header)
        return True

    ##
    ##
    ##
    def ObtainParams(self, obj_args, args):

        args_header = [args[i][0] for i in range(len(args))]
        params = {}
        for i, arg in enumerate(args):
            param = {}
            if   args[i][1] == 'LineEdit':
                param = obj_args[i].text()
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
            elif args[i][1] == 'Tab':
                param = obj_args[i].currentIndex()
            elif args[i][1] == 'CheckBox':
                param = obj_args[i].checkState()
            params[args_header[i]] = param
        return params



    def ObtainTarget(self):

        ## Obtain parameters

        params = self.ObtainParams(self.obj_args, self.args)
        #
        input_path = params['Target Folder']
        #
        search1 = os.path.join(input_path, '*.png')
        search2 = os.path.join(input_path, '*.tif')
        search3 = os.path.join(input_path, '*.tiff')
        filestack = sorted(glob.glob(search1))
        filestack.extend(sorted(glob.glob(search2)))
        filestack.extend(sorted(glob.glob(search3)))
        return filestack

    ##