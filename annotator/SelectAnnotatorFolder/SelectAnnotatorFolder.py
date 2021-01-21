

from PyQt5.QtWidgets import QMessageBox, QWidget, QSizePolicy, QComboBox, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import socket
import sys
import os
import threading

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(path.join(main_dir, "annotator"))

import miscellaneous.Miscellaneous as m
from annotator.Annotator.ControlAnnotatorServer import ControlAnnotatorServer


from miscellaneous.SharedFileDialogs import SharedFileDialogs
from miscellaneous.SyncListQComboBoxManager import *
# import wxglade_superpixel

# class GenerateDialog(QWidget):

class _GenerateContents(SharedFileDialogs):

    def __init__(self, parent):
        self.parent = parent

    def generate(self):
        lbl   = QLabel('Select Annotator Folder.')
        edit  = SyncListQComboBoxDojoManager.get().create(self, 0)
        btn   = QPushButton("Open...")
        btn.clicked.connect(lambda state : self.browse_OpenSpecificFolder(edit, ['Annot']) )
        return lbl, edit, btn


class GenerateDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.u_info = parent.u_info
        
        ## Dialog: Is the 3D Viewer already launched?
        if 'annotator' in self.parent.table_widget.appl:
            msg = QMessageBox(QMessageBox.Information, "3D Annotator", "3D Annotator has already been launched!")
            msg.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
            exe = msg.exec_()
            return None

        
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

        if self.parent.CheckFolderDojo(dir_Annotator) != 1:
            print('Not a Annotator folder.')
            return False

        self.u_info.port_annotator = self.u_info.port_annotator + 1
        self.u_info.SetUserInfoAnnotator(dir_Annotator)
        self.u_info.annotator_files_found = True
        ##
        ##
        self.parent.annotator = ControlAnnotatorServer(self.parent)
        self.parent.annotator.LaunchAnnotator()
        self.close()
        return True

    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False


