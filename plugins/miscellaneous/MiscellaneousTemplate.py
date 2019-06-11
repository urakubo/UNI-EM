##
##
##
import sys, os, time, errno
import h5py
import cv2
import png
from itertools import product
import glob
import threading

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
filesystem_dir = path.join(main_dir, "filesystem")
gui_dir = path.join(main_dir, "gui")
sys.path.append(segmentation_dir)
sys.path.append(filesystem_dir)
sys.path.append(gui_dir)

from FileSystem import FileSystem
from miscellaneous.SharedFileDialogs import SharedFileDialogs
import miscellaneous.Miscellaneous as m


class MiscellaneousTemplate(SharedFileDialogs):


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


    def Execute(self, parent, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)
        thread = threading.Thread(target=self._Run, args=( params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent.parent, 'Template',  comm_title + ' runs on a different process.')
        # parent.close()
        return

    def Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.parent.close()
        return False

