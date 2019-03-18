
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


# ----------------------------------------------------------------------
# Interface of plugins to Control Panel
# Please add user defined functions
# Also please edit "menu.json" for a plugins pulldown menu.
# ----------------------------------------------------------------------

#sys.path.append(path.join(plugins_dir, "superpixel"))
sys.path.append(path.join(plugins_dir, "_2D_watershed"))
sys.path.append(path.join(plugins_dir, "_3D_filters"))
sys.path.append(path.join(plugins_dir, "_2D_filters"))
from Dialog_2D_Watershed import Dialog_2D_Watershed
from Dialog_3D_Filters import Dialog_3D_Filters
from Dialog_2D_Filters import Dialog_2D_Filters

# import wxglade_superpixel

class Plugins():

    def _2D_Filters(self):
        self.tmp = Dialog_2D_Filters(self)

    def _2D_Watershed(self):
        self.tmp = Dialog_2D_Watershed(self)

    def _3D_Filters(self):
        self.tmp = Dialog_3D_Filters(self)

    def SuperPixel_(self):
        #import wx
        # self.superpix = wxglade_superpixel.SuperPixel(self, wx.ID_ANY, "",sim_name=[self, self.UserInfo])
    	#self.superpix = wxglade_superpixel.SuperPixel(self, wx.ID_ANY, "")
        #self.superpix.Show()
        #event.Skip()
        pass

    def UserDefined_(self):
        print("'User Defined' is not implemented!")
        # event.Skip()

# ----------------------------------------------------------------------

