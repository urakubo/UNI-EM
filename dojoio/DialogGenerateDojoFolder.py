###
###
###

import sys, os, time, errno


import numpy as np
import copy
import subprocess as s
import time


from os import path, pardir
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy,QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

main_dir    = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir    = path.join(main_dir, "icons")
# plugins_dir = path.join(main_dir, "plugins")
# sys.path.append(plugins_dir)
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "system"))
# sys.path.append(os.path.join(main_dir, "gui"))

from Params import Params
from ImportImgSeg import ImportImgSeg
from miscellaneous.SharedFileDialogs import SharedFileDialogs
from miscellaneous.SyncListQComboBoxManager import *
import miscellaneous.Miscellaneous as m

class _GenerateContents(SharedFileDialogs):

    def __init__(self, parent):
        self.parent = parent
        self.args = [
                        'Source Image Folder:<BR>(TIFF/PNG)',
                        'Source Segmentation Folder:<BR>(TIFF/PNG)',
                        'Destination Dojo Folder:'
                    ]

    def generate(self, i):
        lbl   = QLabel(self.args[i])
        edit  = SyncListQComboBoxExcludeDojoMtifManager.get().create(self, i)
        btn   = QPushButton("Open...")
        btn.clicked.connect(lambda state : self.browse_OpenImageFolder(edit) )
        return lbl, edit, btn


#class DialogGenerateDojoFolder(QWidget):
class DialogGenerateDojoFolder(QDialog):

    def __init__(self, parent, u_info):
        super().__init__()
        self.parent = parent
        self.u_info = u_info
        self.title = 'Create Dojo Folder'
        self.left = 200
        self.top = 200
        self.width = 700
        self.height = 150

        self.initUI()

    def initUI(self):

        lbl         = [0,0,0]
        self.edit   = [0,0,0]
        btn         = [0,0,0]

        content = _GenerateContents(self)
        for i in range(3):
            lbl[i], self.edit[i], btn[i] = content.generate(i)

        ok_import = QPushButton("OK")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ok_import.clicked.connect(self._ExecuteImport)
        cl_import.clicked.connect(self._Cancel)

        self.em_only = QCheckBox('Use blank segmentation')

        self.edit[1].setEnabled(self.em_only.checkState() == Qt.Unchecked)
        self.em_only.stateChanged.connect(self._CheckEMOnly)


        layout = QGridLayout()

        for i in range(3):
            layout.addWidget(lbl[i], i, 0)
            layout.addWidget(self.edit[i], i, 1, 1, 2)
            layout.addWidget(btn[i], i, 3)

        layout.addWidget(self.em_only, 3, 1, alignment=(Qt.AlignLeft))

        layout.addWidget(ok_import, 3, 2, alignment=(Qt.AlignRight))
        layout.addWidget(cl_import, 3, 3)

        self.setLayout(layout)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.show()


    def _CheckEMOnly(self):
        self.edit[1].setEnabled(self.em_only.isChecked() == Qt.Unchecked)
#        if self.em_only.isChecked() == Qt.Unchecked:
#            self.edit2.setEnabled(True)
#        else:
#            self.edit2.setEnabled(False)



    def _ExecuteImport(self):  # wxGlade: ImportImagesSegments.<event_handler>
        dir_input_images = self.edit[0].currentText()
        dir_input_ids    = self.edit[1].currentText()
        dir_dojo         = self.edit[2].currentText()
        self.u_info.SetUserInfo(dir_dojo)

        if len(dir_input_images) == 0 :
                print('No input image.')
                return

        ##
        if (self.em_only.isChecked() == Qt.Unchecked) and (len(dir_input_ids) != 0):
        ##
            im = ImportImgSeg(self.u_info)
            Flag1 = im.images(dir_input_images)  ###
            Flag2 = im.ids(dir_input_ids)        ###
            #print(Flag1)
            #print(Flag2)
            if Flag1 == False or Flag2 == False:
                print('Error! Dojo files were not created.')
                self.close()
                return False
            print('Dojo files were successfully created.')
            ## File system update
            self._UpdateFileSystem(dir_dojo)
            self.close()
        ##
        else :
        ##
            im = ImportImgSeg(self.u_info)
            Flag1 = im.images(dir_input_images)  ###
            Flag2 = im.ids_dummy(dir_input_images)  ###
            #print(Flag1)
            #print(Flag2)
            if Flag1 == False or Flag2 == False:
                print('Error! Dojo files were not created.')
                self.close()
                return False
            print('Dojo files were successfully created.')
            ## File system update
            self._UpdateFileSystem(dir_dojo)
            ##
            self.close()
        ##
        self.close()
        return False


    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False


    def _UpdateFileSystem(self, dir_dojo):
        # Release
        m.UnlockFolder(self.u_info, dir_dojo)
        # Lock again
        m.LockFolder(self.u_info, dir_dojo)
        # Filetype
        self.u_info.open_files_type[dir_dojo] = 'Dojo'
        # Dropdown menu update
        self.parent.UpdateOpenFileMenu()
        # Combo box update
        SyncListQComboBoxExcludeDojoMtifManager.get().removeModel(dir_dojo)
        SyncListQComboBoxOnlyDojoManager.get().addModel(dir_dojo)


