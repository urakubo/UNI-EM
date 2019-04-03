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
sys.path.append(segmentation_dir)

class _MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DecorationRole:
            return QIcon(QPixmap(self.listdata[index.row()]))
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(os.path.splitext(os.path.split(self.listdata[index.row()])[-1])[0])
        else:
            return QVariant()

class _Dialog_ImageFolder():
    def __init__(self, parent, title, init_path):
        self.w = QDialog(parent)

        self.parent = parent
        self.left   = 300
        self.top    = 300
        self.width  = 600
        self.height = 400
        self.title  = title

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(init_path)
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.treeview = QTreeView()
        self.treeview.setModel(self.dirModel)
        self.treeview.setRootIndex(self.dirModel.index(""))
        self.treeview.clicked.connect(self.on_clicked)
        #--- Hide All Header Sections Except First ----
        header = self.treeview.header()
        for sec in range(1, header.count()):
            header.setSectionHidden(sec, True)
        #--- ---- ---- ---- ---- ---- ---- ---- ---- --

        focus_index = self.dirModel.index(init_path)
        self.treeview.setCurrentIndex(focus_index)
        self.current_row_changed()

        self.listview = QListView()
        self.listview.setViewMode(QListView.IconMode)
        self.listview.setIconSize(QSize(192,192))

        targetfiles1 =  glob.glob(os.path.join( init_path, '*.png'))
        targetfiles2 =  glob.glob(os.path.join( init_path, '*.tif'))
        targetfiles3 =  glob.glob(os.path.join( init_path, '*.tiff'))
        targetfiles  = targetfiles1 + targetfiles2 + targetfiles3
        lm = _MyListModel(targetfiles, self.parent)
        self.listview.setModel(lm)

        self.sub_layout = QHBoxLayout()
        self.sub_layout.addWidget(self.treeview)
        self.sub_layout.addWidget(self.listview)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.sub_layout)
        self.main_layout.addWidget(self.buttonBox)

        self.w.setGeometry(self.left, self.top, self.width, self.height)
        self.w.setWindowTitle(self.title)
        self.w.setWindowIcon(QIcon(os.path.join(icon_dir, 'Mojo2_16.png')))
        self.w.setLayout(self.main_layout)

    def current_row_changed(self):
        index = self.treeview.currentIndex()
        self.treeview.scrollTo(index, QAbstractItemView.EnsureVisible)
        self.treeview.resizeColumnToContents(0)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()

        targetfiles1 =  glob.glob(os.path.join( path, '*.png'))
        targetfiles2 =  glob.glob(os.path.join( path, '*.tif'))
        targetfiles3 =  glob.glob(os.path.join( path, '*.tiff'))
        targetfiles  = targetfiles1 + targetfiles2 + targetfiles3

        lm = _MyListModel(targetfiles, self.parent)
        self.listview.setModel(lm)

    def accept(self):
        index = self.treeview.currentIndex()
        self.newdir = self.dirModel.filePath(index)
        self.w.done(1)

    def reject(self):
        self.w.done(0)

    def GetValue(self):
        index = self.treeview.currentIndex()
        self.newdir = self.dirModel.filePath(index)
        return self.newdir


class MiscellaneousTemplate():

    def browse_dir_img(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        Dialog = _Dialog_ImageFolder(self, "Select Image Folder",  currentdir)
        return_flag = Dialog.w.exec_()
        if return_flag == 1:
            newdir = Dialog.GetValue()
            lineedit_obj.setText(newdir)
            return True
        return False


    def browse_dir(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        newdir = QFileDialog.getExistingDirectory(self, "Select Folder", currentdir)
        if len(newdir) == 0:
            return False
        newdir = newdir.replace('/', os.sep)
        lineedit_obj.setText(newdir)
        return True


    def browse_file(self, lineedit_obj):
        currentfile = lineedit_obj.text()
        newfile = QFileDialog.getOpenFileName(self, "Select File", currentfile)
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
    def ObtainCroppedImage(self, input_image, sx, sy, W, H, MAXSLIDER):
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
    def GenerateTabWidget(self, filter):

        args        = filter.args
        tips        = filter.tips
        paramfile   = filter.paramfile
        filter_name = filter.name
        fexecute    = filter.Execute

        args.extend([
                        ['Save Parameters', 'LineEdit',paramfile, 'BrowseFile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'BrowseFile']
                    ])

        tips.extend([
                        'Save Parameters ',
                        'Load Parameters '
                    ])


        lbl      = []
        obj_args = []

        for i in range(len(args)):
            arg = args[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda : self.save_params(obj_args, args, filter_name))
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda : self.load_params(obj_args, args, filter_name))
            else :
                lbl.append(QLabel(args[i][0] + ' :'))
                lbl[-1].setToolTip(tips[i])

        require_browse_dir     = []
        require_browse_dir_img = []
        require_browse_file    = []
        for i in range(len(args)):
            if  args[i][1] == 'LineEdit':
                obj_args.append( QLineEdit() )
                obj_args[-1].setText( args[i][2] )
                if args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                if args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                if args[i][3] == 'BrowseFile':
                    require_browse_file.append(i)
            elif args[i][1] == 'SpinBox':
                obj_args.append(QSpinBox())
                obj_args[-1].setMinimum( args[i][2][0] )
                obj_args[-1].setMaximum( args[i][2][2] )
                obj_args[-1].setValue( args[i][2][1] )
            elif args[i][1] == 'ComboBox':
                obj_args.append(QComboBox())
                items = args[i][2]
                for item in items:
                    obj_args[-1].addItem(item)
            elif args[i][1] == 'CheckBox':
                obj_args.append(QCheckBox(''))
                obj_args[-1].setChecked( args[i][2] )
            else:
                print('Internal error. No fucntion.')

        tab = QWidget()
        tab.layout = QGridLayout(tab)
        ncol = 8
        browse_button = []
        for id in range(len(lbl)):
            tab.layout.addWidget(lbl[id], id + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            tab.layout.addWidget(obj_args[id], id + 1, 1, 1, ncol - 1)
            if id in require_browse_dir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_dir(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_img:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_dir_img(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_file(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))


                # addWidget(*Widget, row, column, rowspan, colspan)

        ## Execute & cancel buttons
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(lambda: fexecute(self, filter_name, obj_args, args ))
        cl_import.clicked.connect(self.Cancel)
        tab.layout.addWidget(ok_import, len(lbl) + 2, 1, alignment=(Qt.AlignRight))
        tab.layout.addWidget(cl_import, len(lbl) + 2, 2)
        tab.layout.setRowStretch(20, 1) # I do not understand why >(5, 1) produces top aligned rows.
        tab.setLayout(tab.layout)

        return tab

    def Execute(self, parent, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)
        thread = threading.Thread(target=self._Run, args=( params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent, 'Template',  comm_title + ' runs on a different process.')
        # parent.close()
        return

    def Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False



