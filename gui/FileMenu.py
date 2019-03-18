
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

import json
from  collections import OrderedDict

from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QWidget, QPushButton, QAction, QMessageBox, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))


class FileMenu():
# class MainWindow(QMainWindow, Credit, Plugins):

    def __init__(self):


        # File menu
        self.file_menu_ = ['Import EM Stack/Segmentation',
                   'Open Dojo Folder',
                   'Close Dojo Folder',
                   'Save Dojo Folder',
                   'Export Dojo Folder',
                   'Export EM Stack',
                   'Export Segmentation',
                   'Exit']

        self.file_icon = ['Photo_Import_16.png',
                  'Folder_16.png',
                  'Close_16.png',
                  'Save_16.png',
                  'Folder_Right_16.png',
                  'Photo_Right_16.png',
                  'Object_Right_16.png',
                  'Power_Off_16.png']

        self.file_icon_diabled = ['Photo16.png',
                          'Folder16.png',
                          'Close16.png',
                          'Save16.png',
                          'Folder16.png',
                          'Photo16.png',
                          'Object16.png',
                          'PowerOff16.png']
        self.act_file_icon_init = [1, 1, 0, 0, 0, 0, 0, 1]
        self.act_file_icon_open = [0, 0, 1, 1, 1, 1, 1, 1]

        self.file_action = [self.Import,
                          self.SelectDojoFile,
                          self.CloseDojoFiles,
                          self.SaveDojoFiles,
                          self.ExportDojoFiles,
                          self.ExportImages,
                          self.ExportSegmentation,
                          qApp.quit]

    def InitialzeFileMenu(self, file_folder):
        file_id = []
        # for menu, icon, icon_diabled in zip(self.file_menu_, self.file_icon, self.file_icon_diabled) :
        for menu, icon, icon_diabled, action in zip(self.file_menu_, self.file_icon, self.file_icon_diabled, self.file_action) :
            # print(path.join(main_dir, icon))
            ii = QIcon()
            ii.addPixmap(QPixmap(path.join(icon_dir, icon)), QIcon.Normal, QIcon.On)
            ii.addPixmap(QPixmap(path.join(icon_disabled_dir, icon_diabled)), QIcon.Disabled)
            id = QAction(ii, menu, self)
            # id = QAction(QIcon(path.join(icon_dir, icon)), menu, self)
            file_id.append(id)
            id.triggered.connect(action)
            file_folder.addAction(id)
        return file_id

    def InitModeFileMenu(self, file_id):
        for i, id in enumerate(file_id) :
            id.setEnabled(self.act_file_icon_init[i])
            id.setDisabled(1-self.act_file_icon_init[i])

    def ActiveModeFileMenu(self, file_id):
        for i, id in enumerate(file_id) :
            id.setEnabled(self.act_file_icon_open[i])
            id.setDisabled(1-self.act_file_icon_open[i])
