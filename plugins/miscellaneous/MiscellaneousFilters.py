##
##
##

import dill
import sys, os, time, errno
import h5py
import cv2
import png
from itertools import product
import glob
import copy

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

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(main_dir)
sys.path.append(segmentation_dir)

import miscellaneous.Miscellaneous as m

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

        # path = QDir.rootPath()

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(init_path)
        #==========
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.treeview = QTreeView()
        #self.dirModel.setFilter(QDir.AllDirs)
        #self.treeview = QTableView()
        #==========
        self.treeview.setModel(self.dirModel)
        #treeview.setRootIndex(self.dirModel.index(QDir.rootPath()))
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
        # self.w.exec_()

    def current_row_changed(self):
        index = self.treeview.currentIndex()
        self.treeview.scrollTo(index, QAbstractItemView.EnsureVisible)
        self.treeview.resizeColumnToContents(0)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        # self.listview.setRootIndex(self.fileModel.setRootPath(path))
        # print('Path:   ', path)

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
        #return True

    def reject(self):
        self.w.done(0)
        #return False

    def GetValue(self):
        index = self.treeview.currentIndex()
        self.newdir = self.dirModel.filePath(index)
        return self.newdir


class MiscellaneousFilters():
    ##
    def browse_dir_img(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        Dialog = _Dialog_ImageFolder(self.parent, "Select Image Folder",  currentdir)
        return_flag = Dialog.w.exec_()
        if return_flag == 1:
            newdir = Dialog.GetValue()
            lineedit_obj.setText(newdir)
            return True
        return False

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


    def save_params(self, args, obj_args):
        #
        args_header = [args[i][0] for i in range(len(args))]
        id = args_header.index('Save Parameters')
        filename = obj_args[id].text()
        print('\nSave file : ', filename)
        print()

        # Obtain paraems for save
        w = self.parent.targetWidget
        texts = []
        instances = []
        for i in range(w.count()):
            item = w.item(i)
            texts.append( item.text() )
            instances.append( item.data(Qt.UserRole) )
        print('Texts: ', texts)
        print('Instances: ', instances)
        try:
            with open(filename, mode='wb') as f:
                pickle.dump([texts, instances], f)
            print(filename, ': Parameter file was saved.')
        except :
            print(filename, ': Parameter file could not be saved.')
            return False

        return True


    def load_params(self, args, obj_args):
        #
        args_header = [args[i][0] for i in range(len(args))]
        id = args_header.index('Load Parameters')
        filename = obj_args[id].text()
        print('\nLoad file : ', filename)
        print()
        try:
            with open(filename, mode='rb') as f:
                [texts, instances] = pickle.load(f)
        except :
            print(filename, ': Parameter file cannot be open.')
            return False

        for text, instance in zip(texts, instances):
            print('Loaded', text, instance)

        # w = self.parent.listManager
        # for instance in instances:
        #    w.addFilter(instance)

        return True

    ##
    ##
    ##
    def ObtainParams(self, args):
        args_header = [args[i][0] for i in range(len(args))]
        params = {}
        for i, arg in enumerate(args):
            if   args[i][1] == 'LineEdit':
                param = args[i][2][1]
            elif args[i][1] == 'SpinBox':
                param = args[i][2][1]
            elif args[i][1] == 'ComboBox':
                param = args[i][2][0]
            elif args[i][1] == 'CheckBox':
                param = args[i][2]
            params[args_header[i]] = param
        return params


    def ObtainParamsBottomTable(self, obj_args, args):
        args_header = [args[i][0] for i in range(len(args))]
        params = {}
        for i, arg in enumerate(args):
            params[args_header[i]] = obj_args[i].text()
        return params



    def ObtainTarget(self):

        ## Obtain parameters

        params = self.ObtainParamsBottomTable(self.obj_args, self.args)
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


    def Execute3D(self, w):
        ##
        ## Load image
        ##
        filestack = self.ObtainTarget()
        params = self.ObtainParamsBottomTable(self.obj_args, self.args)
        output_path = params['Output Folder']
        numz = len(filestack)
        size = cv2.imread(filestack[0], cv2.IMREAD_GRAYSCALE).shape
        input_volume = np.zeros([size[0], size[1], numz], np.uint16)

        print('Loading images ...')
        for zi, filename in enumerate(filestack):
            input_volume[:, :, zi] = cv2.imread(filename, cv2.IMREAD_GRAYSCALE).astype(np.uint16)
        ##
        ## 2D/3D filter application
        ##
        for i in range(w.count()):
            item = w.item(i)
            text = item.text()
            instance = item.data(Qt.UserRole)
            params = self.ObtainParams(instance.args)
            type = self.fi.get_type(text)
            cls = self.fi.get_class(text)

            if type == '2d':
                for zi in range(numz):
                    input_image = input_volume[:, :, zi]
                    output_image = cls.Filter(self, input_image, params)
                    input_volume[:, :, zi] = output_image.astype(np.uint16)
            elif type == '3d':
                tmp = cls.Filter(self, input_volume, params)
                input_volume = tmp.astype(np.uint16)

        # Save segmentation
        print('Saving images ...')
        for zi, filename in enumerate(filestack):
            output_name = os.path.basename(filename)
            savename = os.path.join(output_path, output_name)
            root, ext = os.path.splitext(savename)
            if ext == ".tif" or ext == ".tiff" or ext == ".TIF" or ext == ".TIFF":
                m.save_tif16(input_volume[:, :, zi], savename)
            elif ext == ".png" or ext == ".PNG":
                m.save_png16(input_volume[:, :, zi], savename)
        print('2D/3D filters were applied!')

    def Execute2D(self, w):
        ##
        ## Input files /Output folder
        ##
        self.filestack = self.ObtainTarget()
        params = self.ObtainParamsBottomTable(self.obj_args, self.args)
        output_path = params['Output Folder']
        for filename in self.filestack:
            output_name = os.path.basename(filename)
            print(output_name)
            input_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            output_image = self.FilterApplication2D(w, input_image)
            output_dtype = output_image.dtype
            savename = os.path.join(output_path, output_name)
            root, ext = os.path.splitext(savename)
            if ext == ".tif" or ext == ".tiff" or ext == ".TIF" or ext == ".TIFF":
                if output_dtype == 'uint16':
                    m.save_tif16(output_image, savename)
                elif output_dtype == 'uint8':
                    m.save_tif8(output_image, savename)
                else:
                    print('dtype mismatch: ', output_dtype)
            elif ext == ".png" or ext == ".PNG":
                if output_dtype == 'uint16':
                    m.save_png16(output_image, savename)
                elif output_dtype == 'uint8':
                    m.save_png8(output_image, savename)
                else:
                    print('dtype mismatch: ', output_dtype)
        print('2D filters were applied!')



    def FilterApplication2D(self, w, image):
        for i in range(w.count()):
            item = w.item(i)
            text = item.text()
            instance = item.data(Qt.UserRole)
            params   = self.ObtainParams(instance.args)
            type = self.fi.get_type(text)
            # print( text, params, type )
            cls = self.fi.get_class(text)
            image = cls.Filter( self, image, params )
        return image

    ##