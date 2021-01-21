import sys, os, time, errno

import numpy as np
import copy
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import tornado
import tornado.websocket

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, QCheckBox, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
from miscellaneous.SyncListQComboBoxManager import *
from miscellaneous.SharedFileDialogs import SharedFileDialogs


sys.path.append( path.join(main_dir, "miscellaneous") )

class TabGenerator(SharedFileDialogs):

    def __init__(self, parent):
        self.parent = parent

    def GenerateTabWidget(self, att):

        args = att.args
        tips = att.tips
        paramfile = att.paramfile
        title = att.title
        _Run = att._Run

        args.extend([
            ['Save Parameters', 'LineEdit', paramfile, 'BrowseFile'],
            ['Load Parameters', 'LineEdit', paramfile, 'BrowseFile']
        ])

        tips.extend([
            'Save Parameters ',
            'Load Parameters '
        ])

        lbl = []
        obj_args = []

        for i in range(len(args)):
            arg = args[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda: self.save_params(obj_args, args, title))
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda: self.load_params(obj_args, args, title))
            else:
                lbl.append(QLabel(args[i][0] + ' :'))
                lbl[-1].setToolTip(tips[i])

        require_browse_dir       = []
        require_browse_dir_img   = []
        require_browse_file      = []
        require_browse_open_img  = []

        require_browse_dir_specific = {}
        require_browse_file_specific = {}

        tab_elem_count = 0
        id_sub_tab = []

        for i in range(len(args)):
            if tab_elem_count > 0:
                current_elem_id = tab_num_elem - tab_elem_count
                tab_elem_count = tab_elem_count - 1
                current_tab_id = tab_elem[current_elem_id]
                obj_args.append(QSpinBox())
                obj_args[-1].setMinimum( args[i][2][0] )
                obj_args[-1].setMaximum( args[i][2][2] )
                obj_args[-1].setValue( args[i][2][1] )
                # print('tab_count      : ', tab_count)
                # print('current_elem_id: ', current_elem_id)
                # print('current_tab_id : ', current_tab_id)
                # print('tab_row[current_tab_id] : ', tab_row[current_tab_id])
                ttab[current_tab_id].layout.addWidget(lbl[i], tab_row[current_tab_id], 0, alignment=(Qt.AlignRight))
                ttab[current_tab_id].layout.addWidget(obj_args[-1], tab_row[current_tab_id], 1, 1, 4)
                tab_row[current_tab_id] = tab_row[current_tab_id] + 1
                id_sub_tab.append(i)
            elif args[i][1] == 'LineEdit':
                obj_args.append(QLineEdit())
                obj_args[-1].setText(args[i][2])
                if args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                if args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                if args[i][3] == 'BrowseFile':
                    require_browse_file.append(i)
            elif args[i][1] == 'LineEdit_number':
                obj_args.append(QLineEdit())
                # (min, Default value, max, Number of digits)
                obj_args[-1].setValidator(QDoubleValidator(\
                        	args[i][2][0],\
        					args[i][2][2],\
        					args[i][2][3],\
        					notation=QDoubleValidator.StandardNotation))
                obj_args[-1].setText(str(args[i][2][1]))
            elif args[i][1] == 'SpinBox':
                obj_args.append(QSpinBox())
                obj_args[-1].setMinimum(args[i][2][0])
                obj_args[-1].setMaximum(args[i][2][2])
                obj_args[-1].setValue(args[i][2][1])
            elif args[i][1] == 'ComboBox':
                obj_args.append(QComboBox())
                items = args[i][2]
                for item in items:
                    obj_args[-1].addItem(item)
            elif args[i][1] == 'CheckBox':
                obj_args.append(QCheckBox(''))
                obj_args[-1].setChecked(args[i][2])
            elif args[i][1] == 'Tab':
                obj_args.append(QTabWidget())
                tab_num = len(args[i][2])
                tab_elem = args[i][3]
                tab_num_elem = len(args[i][3])
                tab_elem_count = tab_num_elem
                tab_row = [0 for i in range(tab_num)]
                ttab = []
                for j in range(tab_num):
                    ttab.append(QWidget())
                    obj_args[-1].addTab(ttab[-1], args[i][2][j])
                    ttab[-1].layout = QGridLayout(ttab[-1])
                    ttab[-1].setLayout(ttab[-1].layout)
            ##
            elif args[i][1] == 'SelectImageFolder':
                obj_args.append(SyncListQComboBoxImageManager.get().create(att, i))
                if args[i][2] == 'OpenImageFolder':
                    require_browse_open_img.append(i)
            elif args[i][1] == 'SelectModelFolder':
                obj_args.append(SyncListQComboBoxModelManager.get().create(att, i))
                if args[i][2] == 'OpenModelFolder':
                    require_browse_dir_specific[i] = 'Model'
            elif args[i][1] == 'SelectDojoFolder':
                obj_args.append(SyncListQComboBoxDojoManager.get().create(att, i))
                if args[i][2] == 'OpenDojoFolder':
                    require_browse_dir_specific[i] = 'Dojo'
            elif args[i][1] == 'SelectFFNsFolder':
                obj_args.append(SyncListQComboBoxFFNsManager.get().create(att, i))
                if args[i][2] == 'OpenFFNsFolder':
                    require_browse_dir_specific[i] = 'FFNs'
            elif args[i][1] == 'SelectHdf5File':
                obj_args.append(SyncListQComboBoxHdf5Manager.get().create(att, i))
                if args[i][2] == 'OpenHdf5File':
                    require_browse_file_specific[i] = 'hdf5'
            elif args[i][1] == 'SelectEmptyFolder':
                obj_args.append(SyncListQComboBoxEmptyManager.get().create(att, i))
                if args[i][2] == 'OpenEmptyFolder':
                    require_browse_dir_specific[i] = 'Empty'
            elif args[i][1] == 'SelectEmptyModelFolder':
                obj_args.append(SyncListQComboBoxEmptyModelManager.get().create(att, i))
                if args[i][2] == 'OpenEmptyModelFolder':
                    require_browse_dir_specific[i] = ['Empty','Model']
            else:
                print('Internal error. No fucntion.')

        tab = QWidget()
        tab.layout = QGridLayout(tab)
        ncol = 8
        browse_button = []
        i = 0
        for id in range(len(lbl)):
            if id in id_sub_tab :
                continue
            tab.layout.addWidget(lbl[id], i + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            tab.layout.addWidget(obj_args[id], i + 1, 1, 1, ncol - 1)
            if id in require_browse_dir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_dir(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_img:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_dir_img(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_file(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_open_img:
                browse_button.append(QPushButton("Open..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_OpenImageFolder(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_specific.keys():
                browse_button.append(QPushButton("Browse..."))
                folder_type = require_browse_dir_specific[id]
                print('folder_type : ',  folder_type)
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_OpenSpecificFolder(obj_args[z], folder_type))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file_specific.keys():
                browse_button.append(QPushButton("Browse..."))
                file_type = require_browse_file_specific[id]
#                print('file_type : ',  file_type)
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_OpenSpecificFile(obj_args[z], file_type))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))

            i = i + 1
                # addWidget(*Widget, row, column, rowspan, colspan)

        ## Execute & cancel buttons
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(lambda: self.Execute(self.parent, _Run, title, obj_args, args))
        cl_import.clicked.connect(self.Cancel)
        tab.layout.addWidget(ok_import, len(lbl) + 2, 1, alignment=(Qt.AlignRight))
        tab.layout.addWidget(cl_import, len(lbl) + 2, 2)
        tab.layout.setRowStretch(20, 1)  # I do not understand why >(5, 1) produces top aligned rows.
        tab.setLayout(tab.layout)

        return tab


    def Cancel(self):
        self.parent.close()
        return False


    def Execute(self, parent, _Run, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)
        thread = threading.Thread(target=_Run, args=( parent, params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent, 'External function',  comm_title + ' runs on a different thread.')
        # parent.close()
        return


