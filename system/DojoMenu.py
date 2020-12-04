
import sys
import os

import json
from  collections import OrderedDict

from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, qApp, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(os.path.join(main_dir, "system"))
sys.path.append(os.path.join(main_dir, "dojoio"))

from DojoFileIO import DojoFileIO

class DojoMenu( DojoFileIO ):
# class MainWindow(QMainWindow, Credit, Plugins):

    def __init__(self):
        # super(DojoMenu, self).__init__()
        DojoFileIO.__init__(self)
        # File menu
        self.dojo_menu = ['Create Dojo Folder',
                   'Open Dojo Folder',
                   'Close Dojo Folder',
                   'Save Dojo Folder',
                   'Export Dojo Folder',
                   'Export EM Stack',
                   'Export Segmentation']

        self.dojo_icon = ['Photo_right_16.png',
                  'Folder_16.png',
                  'Close_16.png',
                  'Save_16.png',
                  'Folder_Right_16.png',
                  'Photo_Right_16.png',
                  'Object_Right_16.png']

        self.dojo_icon_diabled = ['Photo16.png',
                          'Folder16.png',
                          'Close16.png',
                          'Save16.png',
                          'Folder16.png',
                          'Photo16.png',
                          'Object16.png']
        self.act_dojo_icon_init = [1, 1, 0, 0, 0, 0, 0]
        self.act_dojo_icon_open = [1, 0, 1, 1, 1, 1, 1]

        self.dojo_action = [self.GenerateDojoFolder,
                          self.SelectDojoFile,
                          self.CloseDojoFiles,
                          self.SaveDojoFiles,
                          self.ExportDojoFiles,
                          self.ExportImages,
                          self.ExportSegmentation]

    def DojoDropdownMenu(self, dojo_folder):

        # File menu

        file_id = []
        for menu, icon, icon_diabled, action in zip(self.dojo_menu, self.dojo_icon, self.dojo_icon_diabled, self.dojo_action) :
            ii = QIcon()
            ii.addPixmap(QPixmap(path.join(icon_dir, icon)), QIcon.Normal, QIcon.On)
            ii.addPixmap(QPixmap(path.join(icon_disabled_dir, icon_diabled)), QIcon.Disabled)
            id = QAction(ii, menu, self)
            # id = QAction(QIcon(path.join(icon_dir, icon)), menu, self)
            file_id.append(id)
            id.triggered.connect(action)
            # print('len(dojo_folder): ', len(dojo_folder))
            # print('menu: ', menu)
            dojo_folder.addAction(id)
        return file_id

    def InitModeDojoMenu(self, file_id):
        for i, id in enumerate(file_id) :
            id.setEnabled(self.act_dojo_icon_init[i])
            id.setDisabled(1-self.act_dojo_icon_init[i])

    def ActiveModeDojoMenu(self, file_id):
        for i, id in enumerate(file_id) :
            id.setEnabled(self.act_dojo_icon_open[i])
            id.setDisabled(1-self.act_dojo_icon_open[i])
