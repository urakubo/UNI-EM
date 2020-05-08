###
###
###

import sys, os, time, errno


import numpy as np
import pickle
import subprocess as s


from os import path, pardir
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QInputDialog, QComboBox, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

main_dir    = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir    = path.join(main_dir, "icons")
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "system"))


from Params import Params
from ImportImgSeg import ImportImgSeg
from miscellaneous.SharedFileDialogs import SharedFileDialogs
from miscellaneous.SyncListQComboBoxManager import *
from annotator.Annotator.ControlAnnotatorServer import ControlAnnotatorServer

class _GenerateContents(SharedFileDialogs):

    def __init__(self, parent):
        self.parent = parent

    def generate(self):
        lbl   = QLabel('Select Dojo Folder.')
        edit  = SyncListQComboBoxOnlyDojoManager.get().create(self, 0)
        btn   = QPushButton("Open...")
        btn.clicked.connect(lambda state : self.browse_OpenDojoFolder(edit) )
        return lbl, edit, btn


class DialogOpenAnnotatorFolder(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.u_info = parent.u_info
        self.title = 'Open Annotator Folder'
        self.left = 200
        self.top = 200
        self.width = 400
        self.height = 100

        self.initUI()

    def initUI(self):

        content = _GenerateContents(self)
        lbl, self.edit, btn = content.generate()

        ok_import = QPushButton("OK")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ok_import.clicked.connect(self._ExecuteAnnotator)
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


    def _ExecuteAnnotator(self):  # wxGlade: ImportImagesSegments.<event_handler>
        dir_Annotator = self.edit.currentText()
        if len(dir_Annotator) == 0 :
                print('Folder unspecified.')
                return False
        ##
        if self.parent.parent.CheckFolderDojo(dir_Annotator) != 1:
            print('Not a Annotator folder.')
            return False
        ##
        self.u_info.annotator_files_found = True
        self.u_info.port_annotator = self.u_info.port_annotator + 1
        self.u_info.SetUserInfoAnnotator(dir_Annotator)
        frame_statusbar_fields = "Annotator: " + self.u_info.annotator_files_path
        self.parent.parent.setWindowTitle(frame_statusbar_fields)
        ##

        self.parent.parent.annotator = ControlAnnotatorServer(self.u_info)
        self.parent.parent.annotator.LaunchAnnotator()
        self.parent.parent.table_widget.addTab('annotator', '3D Annotator', self.u_info.url_annotator+'index.html' )

        self.close()
        return True




    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False


    def _UpdateFileSystem(self, dir_annotator):
        # Filetype
        #self.u_info.open_files_type[dir_dojo] = 'Dojo'
        # Release
        for lockfileobj in self.u_info.open_files4lock[dir_annotator].values():
            lockfileobj.close()
        
        # Lock again
        # self.parent.LockFolder(dir_dojo)
        # Dropdown menu update
        self.parent.UpdateOpenFileMenu()
        # Combo box update
        SyncFileListQComboBoxHolder.addModel(dir_annotator)


