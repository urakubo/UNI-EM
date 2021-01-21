###
###
###
import sys, os, time, errno
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QDialog
from PyQt5.QtGui import QIcon
from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "annotator"))

from miscellaneous.TabGenerator import TabGenerator
from annotator.CreateAnnotatorFolder.ImagesTab  import ImagesTab
from annotator.CreateAnnotatorFolder.Hdf5Tab  import Hdf5Tab
from annotator.CreateAnnotatorFolder.DojoTab  import DojoTab

class GenerateDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 600
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "Create Annotator Folder"
        self.initUI()


    def initUI(self):

        ##
        ## Define tab
        ##
        self.layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.resize(300, 500)
        tab_source = TabGenerator(self)

        ##
        ## Images
        ##
        Images    = ImagesTab(self.u_info)
        tab1      = tab_source.GenerateTabWidget(Images) # Widget
        tabs.addTab(tab1, "png/tiff")

        ##
        ## hdf5
        ##
        hdf5      = Hdf5Tab(self.u_info)
        tab2      = tab_source.GenerateTabWidget(hdf5) # Widget
        tabs.addTab(tab2,"hdf5")

        ##
        ## Dojo
        ##
        Dojo      = DojoTab(self.u_info)
        tab2      = tab_source.GenerateTabWidget(Dojo) # Widget
        tabs.addTab(tab2,"Dojo")

        # Add tabs to widget
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()


