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

segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)

from MiscellaneousSegment import MiscellaneousSegment

class TableGeneratorFFN(MiscellaneousSegment):

    def __init__(self, parent):
        self.parent = parent

    def GenerateTableObject(self, filter):

        args = filter.args
        tips = filter.tips
        paramfile = filter.paramfile
        filter_name = filter.filter_name
        ffilter      = filter.Execute

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

        table = QWidget()
        table.layout = QGridLayout(table)
        ncol = 8
        browse_button = []
        for id in range(len(lbl)):
            table.layout.addWidget(lbl[id], id + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            table.layout.addWidget(obj_args[id], id + 1, 1, 1, ncol - 1)
            if id in require_browse_dir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_dir(obj_args[z]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_img:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_dir_img(obj_args[z]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, z=id: self.browse_file(obj_args[z]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))


                # addWidget(*Widget, row, column, rowspan, colspan)

        ## Execute & cancel buttons
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(lambda: ffilter(self.parent, filter_name, obj_args, args ))
        cl_import.clicked.connect(self.Cancel)
        table.layout.addWidget(ok_import, len(lbl) + 2, 1, alignment=(Qt.AlignRight))
        table.layout.addWidget(cl_import, len(lbl) + 2, 2)
        table.layout.setRowStretch(20, 1) # I do not understand why >(5, 1) produces top aligned rows.
        table.setLayout(table.layout)

        return table, obj_args, args


    def Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.parent.close()
        print('3D FFN was not executed.')
        return False

