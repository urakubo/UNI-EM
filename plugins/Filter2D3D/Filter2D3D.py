###
###
###
import sys, os

from PyQt5.QtWidgets import QWidget, QTabWidget, QSizePolicy, \
    QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel,  QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget

from PyQt5.QtGui import QIcon
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
##
import miscellaneous.Miscellaneous as m
from miscellaneous.SyncListQComboBoxManager import *
##
from miscellaneous.MiscellaneousFilters  import MiscellaneousFilters
from miscellaneous.ThumbnailGenerator    import ThumbnailGenerator
from miscellaneous.FilterlistGenerator   import FilterlistGenerator
from miscellaneous.TableGenerator       import TableGenerator

class GenerateDialog(QWidget, MiscellaneousFilters):
    def __init__(self, parent):
        self.left   = 200
        self.top    = 200
        self.width  = 900
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "2D/3D Filters"
        super().__init__()
        self.initUI()

    def initUI(self):
        ###
        ### bottom
        ###

        table1 = TableGenerator(self)
        widget_bottom, obj_args, args = table1.GenerateTableObject()  # Widget

        ###
        ### Top
        ###

        thumb1 = ThumbnailGenerator(self)
        widget_top_right = thumb1.GenerateThumbnailObject(obj_args, args)  # Widget

        self.filter_list = FilterlistGenerator(self)
        widget_top_left  = self.filter_list.GenerateFilterlistObject()  # Widget


        self.targ_image_folder_qcombo.activated.connect( self.ChangeZ )

        widget_top = QWidget()
        widget_top.layout = QHBoxLayout(widget_top)
        widget_top.layout.addWidget(widget_top_left)
        widget_top.layout.addWidget(widget_top_right)

        ###
        ### Connect bottom top
        ###
        widget_all = QWidget()
        widget_all.layout = QVBoxLayout(widget_all)
        widget_all.layout.addWidget(widget_top)
        widget_all.layout.addWidget(widget_bottom)
        self.setLayout(widget_all.layout)

        ##
        ## Generate tabs
        ##

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()
