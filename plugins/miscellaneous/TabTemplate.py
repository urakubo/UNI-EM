from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, QCheckBox, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, \
    QTreeView, QFileSystemModel, QListView, QTableView, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot,  QAbstractListModel, QModelIndex, QVariant, QDir, QSize
import PyQt5.QtGui as QtGui

from MiscellaneousTemplate import MiscellaneousTemplate
from miscellaneous.SyncListQComboBoxManager import *

class TabTemplate(MiscellaneousTemplate):

    def __init__(self, parent):
        self.parent = parent
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
        require_browse_open_img = []
        
        for i in range(len(args)):
            if  args[i][1] == 'LineEdit':
                obj_args.append( QLineEdit() )
                obj_args[-1].setText( args[i][2] )
                if args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                elif args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                elif args[i][3] == 'BrowseFile':
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
            elif args[i][1] == 'SelectOpenImage':
                obj_args.append(SyncListQComboBoxExcludeDjojMtifManager.get().create(filter, i))
                #for item in self.parent.u_info.open_files:
                #    if self.parent.u_info.open_files_type[item] != 'Dojo' :
                #        obj_args[-1].addItem(item)
                if args[i][2] == 'OpenImage':
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
        ok_import.clicked.connect(lambda: fexecute(self, filter_name, obj_args, args ))
        cl_import.clicked.connect(self.Cancel)
        tab.layout.addWidget(ok_import, len(lbl) + 2, 1, alignment=(Qt.AlignRight))
        tab.layout.addWidget(cl_import, len(lbl) + 2, 2)
        tab.layout.setRowStretch(20, 1) # I do not understand why >(5, 1) produces top aligned rows.
        tab.setLayout(tab.layout)

        return tab
