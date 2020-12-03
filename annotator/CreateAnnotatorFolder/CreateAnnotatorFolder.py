

from PyQt5.QtWidgets import QMessageBox, QWidget, QSizePolicy, QComboBox, QDialog, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtCore import Qt

# import socket
import sys
import os
import threading

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(path.join(main_dir, "annotator"))

# import miscellaneous.Miscellaneous as m
from annotator.CreateAnnotatorFolder.FolderCreater import FolderCreater

from miscellaneous.SharedFileDialogs import SharedFileDialogs
from miscellaneous.SyncListQComboBoxManager import *
# import wxglade_superpixel

# class GenerateDialog(QWidget):

class _ComboboxDojo(SharedFileDialogs):
    def __init__(self, parent):
        self.parent = parent
    def Generate(self):
        lbl   = QLabel('Select Dojo Folder.')
        edit  = SyncListQComboBoxDojoManager.get().create(self, 0)
        btn   = QPushButton("Open...")
        btn.clicked.connect(lambda state : self.browse_OpenSpecificFolder(edit, ['Dojo']) )
        return lbl, edit, btn

class GenerateDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.u_info = parent.u_info
        
        self.title = 'Create Annotator Folder'
        self.left = 200
        self.top = 200
        self.width = 400
        self.height = 100

        self.initUI()

    def initUI(self):

        
        self.xpitch = 0.006 ## n um
        self.ypitch = 0.006 ## n um
        self.zpitch = 0.03  ## n um
        
        ok_create = QPushButton("Create")
        cl_create = QPushButton("Cancel")
        ok_create.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_create.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_create.clicked.connect(self._Execute)
        cl_create.clicked.connect(self._Cancel)


        tmp = _ComboboxDojo(self)
        dojo_lbl, self.dojo_edit, dojo_btn = tmp.Generate()

        layout = QGridLayout()  #  self.xpitch, self.ypitch, self.zpitch

        layout.addWidget(dojo_lbl,  0, 0, 1, 2)
        layout.addWidget(self.dojo_edit, 1, 0, 1, 2)
        layout.addWidget(dojo_btn,  1, 2)

        layout.addWidget(QLabel('Specify voxel size in um.'),  2, 0, 1, 2)
        layout.addWidget(QLabel('X (in-slice width) : '),  3, 0, alignment=(Qt.AlignRight))
        layout.addWidget(QLabel('Y (in-slice height) : '),  4, 0, alignment=(Qt.AlignRight))
        layout.addWidget(QLabel('Z (slice thickness) : '),  5, 0, alignment=(Qt.AlignRight))

        obj_xpitch = self._PitchEdit(self.xpitch)
        obj_ypitch = self._PitchEdit(self.ypitch)
        obj_zpitch = self._PitchEdit(self.zpitch)
        layout.addWidget(obj_xpitch,  3, 1)
        layout.addWidget(obj_ypitch,  4, 1)
        layout.addWidget(obj_zpitch,  5, 1)

        layout.addWidget(ok_create, 6, 1, alignment=(Qt.AlignRight))
        layout.addWidget(cl_create, 6, 2)

        self.setLayout(layout)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.show()

    def _PitchEdit(self, default_pitch):
        spinbox = QLineEdit()
        spinbox.setValidator(QDoubleValidator(
        	0.001,	# bottom
        	1.0, 	# top
        	3, 		# decimals
        	notation=QDoubleValidator.StandardNotation))
        spinbox.setText(str(default_pitch))
        return spinbox

    def _Execute(self):
    	##
        self.dir_annotator = self.dojo_edit.currentText()
        if len(self.dir_annotator) == 0 :
                print('Folder unspecified.')
                return False
        if self.parent.CheckFolderDojo(self.dir_annotator) != 1:
            print('Not a Dojo folder.')
            return False
        self.close()
        ##
        annotator_thread = threading.Thread(target=self.StartThreadCreateAnnoatorFolder)
        annotator_thread.setDaemon(True) # Stops if control-C
        annotator_thread.start()
		##
        return True
        ##

    def StartThreadCreateAnnoatorFolder(self):
        logic = FolderCreater(self.u_info, self.dir_annotator, self.xpitch, self.ypitch, self.zpitch )
        logic.Run()

    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False


