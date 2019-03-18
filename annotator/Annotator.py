
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

import socket
import sys
import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
from ControlStlServer import ControlStlServer

#sys.path.append(path.join(plugins_dir, "superpixel"))

# import wxglade_superpixel

class Annotator():

    def Annotator_(self):

        ## Dialog: Is Dojo activated?
        if self.u_info.files_found == False:
            QMessageBox.information(self, "3D Annotator", "Please open Dojo file!")
            return

        ## Dialog: Is the 3D Viewer already launched?
        print( self.table_widget.appl )
        if 'annotator' in self.table_widget.appl:
            QMessageBox.information(self, "3D Annotator", "3D Annotator has already been launched!")
            return

        ## Initialize
        self.u_info.annotator = ControlStlServer(self.u_info)

        ## Start StlServer
        self.u_info.annotator.LaunchStlViewer()

        ## Call StlViewer
        self.table_widget.addTab('annotator', '3D Annotator', self.u_info.url_stl+'index.html' )

    def CloseStlViewer(self):
        ## Start StlServer
        print('Close 3D Annotator')
        self.u_info.annotator.TerminateStlViewer()


