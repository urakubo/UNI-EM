##
##
##

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
    QTreeView, QFileSystemModel, QListView, QTableView, QAbstractItemView, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot,  QAbstractListModel, QModelIndex, QVariant, QDir, QSize
import PyQt5.QtGui as QtGui

from typing import Any

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
#segmentation_dir = path.join(main_dir, "segment")
filesystem_dir = path.join(main_dir, "filesystem")
sys.path.append(main_dir)
#sys.path.append(segmentation_dir)
sys.path.append(filesystem_dir)
#sys.path.append(gui_dir)

from FileSystem import FileSystem
from miscellaneous.SharedFileDialogs import SharedFileDialogs
import miscellaneous.Miscellaneous as m

class MiscellaneousFilters(SharedFileDialogs):
    ##
    ##
    def save_params(self, args, obj_args):
        #
        id = args.index('Save Parameters')
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
        #print('Texts: ', texts)
        #print('Instances: ', instances)
        try:
            with open(filename, mode='wb') as f:
                pickle.dump([texts, instances], f)
            print('Parameters were saved.')
        except :
            print('Parameters could not be saved.')
            return False

        return True


    def load_params(self, args, obj_args):
        #
        id = args.index('Load Parameters')
        filename = obj_args[id].text()
        print('\nLoad file : ', filename)
        print()
        try:
            with open(filename, mode='rb') as f:
                [texts, instances] = pickle.load(f)
        except :
            print(filename, ': Parameter file cannot be open.')
            return False

        targetWidget = self.parent.filter_list.listManager.widgets[2]
        targetWidget.clear()
        for text, instance in zip(texts, instances):
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, instance)
            targetWidget.addItem(item)
            #print('Loaded', text, instance)
        print('Parameters were loaded.')
        return True

    ##
    ##
    ##
    def ObtainParamsFilter(self, args):
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
        params = {}
        print('args: ', args)
        for i in range(len(args)):
            print(obj_args[i].__class__.__name__)
            if obj_args[i].__class__.__name__ == 'QLineEdit':
                params[args[i]] = obj_args[i].text()
            elif obj_args[i].__class__.__name__ == 'SyncListQComboBox':
                params[args[i]] = obj_args[i].currentText()

        return params



    def ObtainTarget(self):

        ## Obtain parameters
        params = self.ObtainParamsBottomTable(self.obj_args, self.args)
        input_path = params['Target Folder']
        ##
        ## Free from filelock
        ##
        # ofolder = self.parent.u_info.open_files4lock.get(input_path)
        # if ofolder == None:
        #    return []
        # for ofileobj in ofolder.values():
        #    ofileobj.close()
        #
        search1 = os.path.join(input_path, '*.png')
        search2 = os.path.join(input_path, '*.tif')
        search3 = os.path.join(input_path, '*.tiff')
        filestack = sorted(glob.glob(search1))
        filestack.extend(sorted(glob.glob(search2)))
        filestack.extend(sorted(glob.glob(search3)))

        # print('filestack : ', filestack)
        return filestack


    def Execute3D(self, w):
        ##
        ## Load image
        ##
        filestack = self.ObtainTarget()
        params = self.ObtainParamsBottomTable(self.obj_args, self.args)
        output_path = params['Output Folder']
        if len(output_path) == 0:
            print('Output folder unspecified.')
            return False
        #
        numz = len(filestack)
        # size = cv2.imread(filestack[0], cv2.IMREAD_GRAYSCALE).shape
        check_attribute = m.imread(filestack[0], flags=cv2.IMREAD_GRAYSCALE)
        tsize  = check_attribute.shape
        tdtype = check_attribute.dtype
        input_volume = np.zeros([tsize[0], tsize[1], numz], tdtype)

        print('Loading images ...')
        for zi, filename in enumerate(filestack):
            # input_volume[:, :, zi] = cv2.imread(filename, cv2.IMREAD_GRAYSCALE).astype(tdtype)
            input_volume[:, :, zi] = m.imread(filename, flags=cv2.IMREAD_GRAYSCALE)
        ##
        ## 2D/3D filter application
        ##
        for i in range(w.count()):
            item = w.item(i)
            text = item.text()
            instance = item.data(Qt.UserRole)
            params = self.ObtainParamsFilter(instance.args)
            type = self.fi.get_type(text)
            cls = self.fi.get_class(text)

            if type == '2d':
                for zi in range(numz):
                    input_image = input_volume[:, :, zi]
                    output_image = cls.Filter(self, input_image, params)
                    input_volume[:, :, zi] = output_image
            elif type == '3d':
                tmp = cls.Filter(self, input_volume, params)
                input_volume = tmp.astype(np.uint16)

        # Unlock Folder
        m.UnlockFolder(self.parent.u_info, output_path)
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
        # Lock Folder
        m.LockFolder(self.parent.u_info, output_path)


    def Execute2D(self, w):
        ##
        ## Input files /Output folder
        ##
        self.filestack = self.ObtainTarget()
        params = self.ObtainParamsBottomTable(self.obj_args, self.args)
        output_path = params['Output Folder']
        if len(output_path) == 0:
            print('Output folder unspecified.')
            return False
        # Unlock Folder
        m.UnlockFolder(self.parent.u_info, output_path)

        for filename in self.filestack:
            print(filename)
            output_name = os.path.basename(filename)
            # input_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            input_image = m.imread(filename, flags=cv2.IMREAD_GRAYSCALE)
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
        # Lock Folder
        m.LockFolder(self.parent.u_info, output_path)


    def FilterApplication2D(self, w, image):
        for i in range(w.count()):
            item = w.item(i)
            text = item.text()
            instance = item.data(Qt.UserRole)
            params   = self.ObtainParamsFilter(instance.args)
            type = self.fi.get_type(text)
            # print( text, params, type )
            cls = self.fi.get_class(text)
            image = cls.Filter( self, image, params )
        return image

    ##
