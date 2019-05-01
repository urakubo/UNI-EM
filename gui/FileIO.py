###
###
###
import sys, os, time, errno


import numpy as np
import copy
#import shutil
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import subprocess as s
import tornado
import tornado.websocket
import time


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "dojo"))
sys.path.append(path.join(main_dir, "plugins"))
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))
plugins_dir = path.join(main_dir, "plugins")

from Params  import Params
from Credit  import Credit
from Plugins import Plugins
from Segment import Segment

from DojoServer import ServerLogic
from ImportDialog import ImportDialog
from SaveChanges import SaveChanges
from ExportImageDialog import ExportImageDialog
from ExportIdDialog import ExportIdDialog

import ExportImgSeg
import asyncio

class FileIO():

#    def StartThreadDojo(self):
#
#        self.p = s.Popen('python -u DojoStandalone.py u_info.pickle', stdout=s.PIPE, stderr=s.PIPE)
#
#        self.sentinel = True
#        while self.sentinel:
#            line = self.p.stdout.readline()
#            if line.strip() == "":
#                pass
#            else:
#                sys.stdout.write(line)
#                sys.stdout.flush()


    def StartThreadDojo(self):
        logic = ServerLogic()
        logic.run(self.u_info)


    def RestartDojo(self):

        print("Asked tornado to exit\n")
        self.u_info.worker_loop.stop()
        time.sleep(1)
        self.u_info.worker_loop.close()

        time.sleep(1)
        print('Restart dojo server.')
        self.u_info.port = self.u_info.port + 1
        print('Port Num: ', self.u_info.port)
        self.u_info.worker_loop = asyncio.new_event_loop()
        self.u_info.dojo_thread = threading.Thread(target=self.StartThreadDojo)
        self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
        self.u_info.dojo_thread.start()

        time.sleep(1)
        self.u_info.url = 'http://' + self.u_info.ip + ':' + str(self.u_info.port) + '/dojo/'
        self.table_widget.addTab('dojo', 'Dojo', self.u_info.url) # ID, Title, URL

    def TerminateDojo(self):

        print("Asked tornado to exit\n")
        # Python3
        self.u_info.worker_loop.stop()
        time.sleep(1)
        self.u_info.worker_loop.close()
        #self.u_info.worker_loop.stop()
        #self.u_info.worker_loop.call_soon_threadsafe(self.u_info.worker_loop.close)
        #self.u_info.dojo_thread.join()

        # if self.u_info.dojo_thread != None:

        self.u_info.dojo_thread = None
        self.u_info.files_found = False
        self.setWindowTitle(self.title)
        self.InitModeFileMenu(self.dojo_icon_open_close)


    def LaunchDojo(self):  # wxGlade: ControlPanel.<event_handler>

        # Launch Dojo server as subprocess.
        #with open(path.join(main_dir, "u_info.pickle"), 'wb') as f:
        #    pickle.dump(self.u_info, f,protocol=2)


        # Python3
        self.u_info.port = self.u_info.port + 1
        print('Port Num: ', self.u_info.port)
        self.u_info.worker_loop = asyncio.new_event_loop()
        self.u_info.dojo_thread = threading.Thread(target=self.StartThreadDojo)
        self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
        self.u_info.dojo_thread.start()

        # self.DojoHTTP.SetURL(self.u_info.url)
        # self.DojoHTTP.SetLabel(self.u_info.url)
        # self.DojoHTTP.SetLabel('Please click here!')
        # self.panel_URL.Show()
        self.ActiveModeFileMenu(self.dojo_icon_open_close)
        # time.sleep(10)
        self.u_info.url = 'http://' + self.u_info.ip + ':' + str(self.u_info.port) + '/dojo/'
        self.table_widget.addTab('dojo', 'Dojo', self.u_info.url) # ID, Title, URL


    def Import(self):  # wxGlade: ControlPanel.<event_handler>
        self.ImportImagesSegments = ImportDialog(self.u_info, self)


    def SelectDojoFile(self):
        dpath = self.u_info.files_path
        fname = QFileDialog.getExistingDirectory(self, "Select Dojo folder", dpath)
        if len(fname) == 0:
            print('No folder was selected.')
            return

        # tmp_info = copy.deepcopy(self.u_info)
        tmp_info = Params()
        tmp_info.SetUserInfo(fname)

        # Check file existence
        if os.path.exists(tmp_info.files_path) and \
            os.path.exists(tmp_info.ids_path) and \
            os.path.exists(tmp_info.tile_ids_path) and \
            os.path.isfile(tmp_info.tile_ids_volume_file) and \
            os.path.isfile(tmp_info.color_map_file) and \
            os.path.isfile(tmp_info.segment_info_db_file) and \
            os.path.exists(tmp_info.images_path) and \
            os.path.exists(tmp_info.tile_images_path) and \
            os.path.isfile(tmp_info.tile_images_volume_file) :
            print('All Dojo files are found. Applying..')
            self.u_info.files_found = True
            self.u_info.SetUserInfo(fname)
        else:
            print('Some Dojo files are missing.')
            return

        # Change statusbar
        frame_statusbar_fields = "Dojo: " + self.u_info.files_path
        self.setWindowTitle(frame_statusbar_fields)

        print(self.u_info.files_path)
        print(self.u_info.ids_path)
        print(self.u_info.tile_ids_path)
        print(self.u_info.tile_ids_volume_file)
        print(self.u_info.color_map_file)
        print(self.u_info.segment_info_db_file)
        print(self.u_info.images_path)
        print(self.u_info.tile_images_path)
        print(self.u_info.tile_images_volume_file)

        self.LaunchDojo()

    def CloseDojoFiles2(self):  # wxGlade: ControlPanel.<event_handler>
        buttonReply = QMessageBox.question(self, 'Closing Dojo File', "Do you want to save changes?",
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            self.SaveChanges = SaveChanges()
            self.SaveChanges.run(self.u_info)
            self.TerminateDojo()
            return(0)
        elif buttonReply == QMessageBox.No:
            self.TerminateDojo()
            return(0)
        else:
            return(1)

    def CloseDojoFiles(self):  # wxGlade: ControlPanel.<event_handler>
        tmp = self.table_widget.appl
        dojo_id = 0
        for i in range(len(tmp)):
            if (tmp[i] == 'dojo'):
                dojo_id = i
        self.table_widget.closeTab(dojo_id)

    def SaveDojoFiles(self):  # wxGlade: ControlPanel.<event_handler>

        self.SaveChanges = SaveChanges()
        self.SaveChanges.run(self.u_info)
        #self.RestartDojo()
        
        # ----------------------------------------------------------------------
    def ExportDojoFiles(self):

        ##
        fname = QFileDialog.getExistingDirectory(self, "Select Export Folder", self.u_info.files_path)
        if len(fname) == 0:
            print('No folder was selected.')
            return
        ##
        dir = fname + os.sep + 'dojo'
        print('Export folder: ', dir)
        tmp_info = Params()
        tmp_info.SetUserInfo(dir)

        print(tmp_info.files_path)
        print(tmp_info.ids_path)
        print(tmp_info.tile_ids_path)
        print(tmp_info.tile_ids_volume_file)
        print(tmp_info.color_map_file)
        print(tmp_info.segment_info_db_file)
        print(tmp_info.images_path)
        print(tmp_info.tile_images_path)
        print(tmp_info.tile_images_volume_file)

        os.mkdir(tmp_info.files_path)
        copy_tree(self.u_info.ids_path, tmp_info.ids_path)
        copy_tree(self.u_info.images_path, tmp_info.images_path)

        # ----------------------------------------------------------------------

    def ExportImages(self):

        self.ImportImagesSegments = ExportImageDialog(self.u_info, self)


        # ----------------------------------------------------------------------
    def ExportSegmentation(self):

        self.ImportIdSegments = ExportIdDialog(self.u_info, self)

        # ----------------------------------------------------------------------

    def Exit(self):  # wxGlade: MojoControlPanel.<event_handler>
        self.Close()
