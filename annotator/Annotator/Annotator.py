

from PyQt5.QtWidgets import  QMessageBox,  QWidget, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

import socket
import sys
import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(path.join(main_dir, "annotator"))
from annotator.Annotator.AnnotatorServer import AnnotatorServerLogic
from annotator.Annotator.ControlAnnotatorServer import ControlAnnotatorServer


# import wxglade_superpixel

class GenerateDialog(QWidget):

    def __init__(self, parent):
        self.u_info = parent.u_info
        self.parent = parent
        super().__init__()
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.initUI()

    def initUI(self):

        ## Dialog: Is Dojo activated?
        if self.u_info.files_found == False:
            QMessageBox.information(self, "3D Annotator", "Please open Dojo file!")
            return

        ## Dialog: Is the 3D Viewer already launched?
        #print( self.parent.table_widget.appl )
        if 'annotator' in self.parent.table_widget.appl:
            QMessageBox.information(self, "3D Annotator", "3D Annotator has already been launched!")
            return

        ## New port
        self.u_info.port_stl = self.u_info.port_stl + 1
        ##
        ## ? Params.SetUserInfo(self, user_path) ? 
        ##
        self.u_info.url_stl  = 'http://' + self.u_info.ip + ':' + str(self.u_info.port_stl) + '/'

        ## Initialize
        self.parent.annotator = ControlAnnotatorServer(self.u_info)

        ## Start StlServer
        self.parent.annotator.LaunchAnnotator()

        ## Call StlViewer
        self.parent.table_widget.addTab('annotator', '3D Annotator', self.u_info.url_stl+'index.html' )


