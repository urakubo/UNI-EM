###
###
###

import sys, os, time, errno


import numpy as np
import copy
#import shutil
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import subprocess as s
import tornado
import tornado.websocket
import time


from os import path, pardir
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QInputDialog, QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

main_dir    = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir    = path.join(main_dir, "icons")
# plugins_dir = path.join(main_dir, "plugins")
# sys.path.append(plugins_dir)
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
# sys.path.append(os.path.join(main_dir, "gui"))

from Params import Params
from ImportImgSeg import ImportImgSeg
from miscellaneous.SharedFileDialogs import SharedFileDialogs
from miscellaneous.SyncFileListQComboBoxHolder import *


class _GenerateContents(SharedFileDialogs):

    def __init__(self, parent):
        self.parent = parent

    def generate(self):
        lbl   = QLabel('Select Dojo Folder.')
        edit  = SyncFileListQComboBoxHolder.create(self, 0)
        btn   = QPushButton("Open...")
        btn.clicked.connect(lambda state : self.browse_OpenDojoFolder(edit) )
        return lbl, edit, btn


#class DialogOpenDojoFolder(QWidget):
class DialogOpenDojoFolder(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.u_info = parent.u_info
        self.title = 'Open Dojo Folder'
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 150

        self.initUI()

    def initUI(self):

        content = _GenerateContents(self)
        lbl, self.edit, btn = content.generate()

        ok_import = QPushButton("OK")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ok_import.clicked.connect(self._ExecuteDojo)
        cl_import.clicked.connect(self._Cancel)


        layout = QGridLayout()


        layout.addWidget(lbl,  0, 0)
        layout.addWidget(self.edit, 1, 0, 1, 2)
        layout.addWidget(btn,  1, 2)

        layout.addWidget(ok_import, 2, 1, alignment=(Qt.AlignRight))
        layout.addWidget(cl_import, 2, 2)

        self.setLayout(layout)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.show()


    def _ExecuteDojo(self):  # wxGlade: ImportImagesSegments.<event_handler>
        dir_Dojo = self.edit.currentText()
        if len(dir_Dojo) == 0 :
                print('Folder unspecified.')
                return False
        ##
        if self.parent.CheckFolderDojo(dir_Dojo) != 1:
            print('Not a Dojo folder.')
            return False
        ##
        self.u_info.files_found = True
        self.u_info.SetUserInfo(dir_Dojo)
        frame_statusbar_fields = "Dojo: " + self.u_info.files_path
        self.parent.setWindowTitle(frame_statusbar_fields)
        self.parent.LaunchDojo()

        self.close()
        return False


    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False


    def _UpdateFileSystem(self, dir_dojo):
        # Filetype
        #self.u_info.open_files_type[dir_dojo] = 'Dojo'
        # Release
        for lockfileobj in self.u_info.open_files4lock[dir_dojo].values():
            lockfileobj.close()
        
        # Lock again
        # self.parent.LockFolder(dir_dojo)
        # Dropdown menu update
        self.parent.UpdateOpenFileMenu()
        # Combo box update
        SyncFileListQComboBoxHolder.addModel(dir_dojo)


    def CloseFolder(self,  dir_dojo):
        tmp_open_files4lock = self.u_info.open_files4lock[dir_dojo]
        for lockfileobj in tmp_open_files4lock.values():
            # print(lockfileobj)
            lockfileobj.close()
        del self.u_info.open_files4lock[dir_dojo]

        self.u_info.open_files.remove(dir_dojo)
        self.UpdateOpenFileMenu()

