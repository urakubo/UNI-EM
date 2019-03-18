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
from MiscellaneousPlugins  import MiscellaneousPlugins
from Executor3D  import Executor3D

class TableGenerator3D(MiscellaneousPlugins):

    def __init__(self, parent):
        self.parent = parent

    def GenerateTableObject(self, filter):

        args = filter.args
        tips = filter.tips
        paramfile = filter.paramfile
        filter_name = filter.filter_name
        output_bitdepth = filter.output_bitdepth
        ffilter      = filter.Filter

        args.extend([
                        ['Save Parameters', 'LineEdit',paramfile, 'Browsefile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'Browsefile']
                    ])

        tips.extend([
                        'Save Parameters',
                        'Load Parameters'
                    ])


        lbl      = []
        obj_args = []

        for i in range(len(args)):
            arg = args[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda: self.save_params(obj_args, args, filter_name))
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda: self.load_params(obj_args, args, filter_name))
            else :
                lbl.append(QLabel(args[i][0] + ' :'))
                lbl[-1].setToolTip(tips[i])

        require_browsedir = []
        require_browsefile = []
        for i in range(len(args)):
            if  args[i][1] == 'LineEdit':
                obj_args.append( QLineEdit() )
                obj_args[-1].setText( args[i][2] )
                if args[i][3] == 'Browsedir':
                    require_browsedir.append(i)
                if args[i][3] == 'Browsefile':
                    require_browsefile.append(i)
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
            if id in require_browsedir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir(obj_args[x]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browsefile:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_file(obj_args[x]))
                table.layout.addWidget(browse_button[-1], id + 1, ncol, 1, 1, alignment=(Qt.AlignRight))


                # addWidget(*Widget, row, column, rowspan, colspan)

        ## Execute & cancel buttons
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(lambda: Executor3D(self.parent, ffilter, filter_name, obj_args, args, output_bitdepth ))
        cl_import.clicked.connect(self.Cancel)
        table.layout.addWidget(ok_import, len(lbl) + 2, 1, alignment=(Qt.AlignRight))
        table.layout.addWidget(cl_import, len(lbl) + 2, 2)
        table.layout.setRowStretch(10, 1) # I do not understand why >(5, 1) produces top aligned rows.
        table.setLayout(table.layout)

        return table, obj_args, args

    ##
    ##

    def Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.parent.close()
        print('3D filter was not executed.')
        return False

