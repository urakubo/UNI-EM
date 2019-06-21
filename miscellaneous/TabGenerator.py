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
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
from miscellaneous.SyncListQComboBoxManager import *

miscellaneous_dir = path.join(main_dir, "miscellaneous")
sys.path.append(miscellaneous_dir)
from SharedFileDialogs import SharedFileDialogs

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

        require_browse_dir = []
        require_browse_dir_img = []
        require_browse_file = []
        require_browse_open_img = []

        for i in range(len(args)):
            if args[i][1] == 'LineEdit':
                obj_args.append(QLineEdit())
                obj_args[-1].setText(args[i][2])
                if args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                if args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                if args[i][3] == 'BrowseFile':
                    require_browse_file.append(i)
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
            elif args[i][1] == 'SelectImageFolder':
                obj_args.append(SyncListQComboBoxExcludeDjojMtifManager.get().create(att, i))
                if args[i][2] == 'OpenImageFolder':
                    require_browse_open_img.append(i)
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
            elif id in require_browse_open_img:
                browse_button.append(QPushButton("Open..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_OpenImageFolder(obj_args[z]))
                tab.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))

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
        QMessageBox.about(parent, 'External function',  comm_title + ' runs on a different process.')
        # parent.close()
        return


