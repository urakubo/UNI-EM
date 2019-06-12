###
###
###
import sys, os, time, errno
#from lockfile import LockFile
#import portalocker

from os import path, pardir
import glob
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))

from DialogGenerateDojoFolder import DialogGenerateDojoFolder

#from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt
from PyQt5.QtWidgets import (QFileDialog, qApp, QMessageBox)
from Params import Params

from miscellaneous.SyncListQComboBoxManager import *
import miscellaneous.Miscellaneous as m

class FileSystem():

    def GenerateDojoFolder(self):
        tmp = DialogGenerateDojoFolder(self, self.u_info)

    def OpenFolder(self):
        initdir = os.path.normpath( path.join(main_dir, "..") )
        open_folder_name = QFileDialog.getExistingDirectory(self, "Select Dojo/Image folder", initdir)
        if len(open_folder_name) == 0:
            print('No folder was selected.')
            return
        open_folder_name = open_folder_name.replace('/', os.sep)
        flag = self.OpenFileFolder(open_folder_name)
        if flag == False:
            return False
        SyncListQComboBoxExcludeDjojMtifManager.get().addModel(open_folder_name)
        SyncListQComboBoxOnlyDojoManager.get().addModel(open_folder_name)


    def OpenRecentFileFolder(self):
        action = self.sender()
        if not action:
            return
        fileName = action.data()
        if not os.path.exists( fileName ):
            QMessageBox.warning(self, "Recent Files",
                                "Cannot find file: %s" % fileName)
            return
        flag = self.OpenFileFolder( fileName )
        if flag == False:
            return False
        SyncListQComboBoxExcludeDjojMtifManager.get().addModel(fileName)
        SyncListQComboBoxOnlyDojoManager.get().addModel(fileName)


    def OpenDropdownFileFolder(self, file_name):
        flag = self.OpenFileFolder( file_name )
        if flag == False:
            return False
        SyncListQComboBoxExcludeDjojMtifManager.get().addModel(file_name)
        SyncListQComboBoxOnlyDojoManager.get().addModel(file_name)


    def OpenMultiTiffFile(self):
        initdir = os.path.normpath( path.join(main_dir, "..") )
        tiff_file = QFileDialog.getOpenFileName(self, "Select Multipage Tiff File", initdir, "TIFF (*.TIF *.tif *.TIFF *.tiff)")
        tiff_file = tiff_file[0]
        if len(tiff_file) == 0:
            return False
        tiff_file = tiff_file.replace('/', os.sep)
        self.OpenFileFolder(tiff_file)


    def Dummy(self):
        pass


    def UpdateOpenFileMenu(self):
        font = QFont("Courier")
        #font.setFixedPitch(True)
        #font.setCapitalization(True)
        font.setPointSize(9)

        num_open_files = min(len(self.u_info.open_files), self.u_info.max_num_open_files)
        for i in range(num_open_files):
            ext  = self.u_info.open_files_type[self.u_info.open_files[i]]
            text = "{0:<6s}{1}".format(ext, self.strippedName(self.u_info.open_files[i]))
            # text = "& {0}  ({1})".format(self.strippedName(self.open_files[i]), ext)
            self.menu_open_files[i].setText(text)
            self.menu_open_files[i].setData(self.u_info.open_files[i])
            self.menu_open_files[i].setVisible(True)
            self.menu_open_files[i].setFont(font)

        for j in range(num_open_files, self.u_info.max_num_open_files):
            self.menu_open_files[j].setVisible(False)

        self.separator1.setVisible((num_open_files > 0))
        self.separator_title.setVisible((num_open_files > 0))
        self.separator2.setVisible((num_open_files > 0))

        return


    def UpdateRecentFileMenu(self):
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        num_recent_files = min(len(files), self.u_info.max_num_recent_files)

        for i in range(num_recent_files):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.menu_recent_files[i].setText(text)
            self.menu_recent_files[i].setData(files[i])
            self.menu_recent_files[i].setVisible(True)

        for j in range(num_recent_files, self.u_info.max_num_recent_files):
            self.menu_recent_files[j].setVisible(False)


    def CloseFileFolder(self, activeAction):
        fileName = activeAction.data()

        if os.path.isdir(fileName):
            m.UnlockFolder(self.u_info, fileName)
        else:
            self.u_info.open_files4lock[fileName].close()
            del self.u_info.open_files4lock[fileName]

        self.u_info.open_files.remove(activeAction.data())
        self.UpdateOpenFileMenu()

        SyncListQComboBoxExcludeDjojMtifManager.get().removeModel(fileName)
        SyncListQComboBoxOnlyDojoManager.get().removeModel(fileName)



    def OpenImageFolder(self, folder_name):

        #### Check open file status
        if not os.path.isdir(folder_name) :
            print('Not a folder.')
            return False

        if self.CheckFolderDojo(folder_name) :
            print('Dojo folder.')
            return False

        return self.OpenFileFolder(folder_name)

    def OpenDojoFolder(self, folder_name):

        #### Check open file status
        if not os.path.isdir(folder_name) :
            print('Not a folder.')
            return False

        if not self.CheckFolderDojo(folder_name) :
            print('Not a Dojo folder.')
            return False

        return self.OpenFileFolder(folder_name)


    def OpenFileFolder(self, fileName):

        #### Check open file status
        if fileName in self.u_info.open_files:
            return False
        if len(self.u_info.open_files) >= self.u_info.max_num_open_files :
            return False

        #### Check file/folder type
        filetype = self.CheckFileType(fileName)
        print('Filetype: ', filetype)
        if filetype == 'invalid':
            print('Invalid file type.')
            return False
        elif filetype == 'multiple type images' :
            print('Folder contains multiple image types.')
            return False

        #### File open
        if os.path.isdir(fileName):
            lock_result = m.LockFolder(self.u_info, fileName)
            if lock_result == False:
                return False
        else:
            try:
                self.u_info.open_files4lock[fileName] = open(fileName, 'r+')
            except:
                print("Cannot open file.")
                return  False

        self.u_info.open_files_type[fileName] = filetype
        self.u_info.open_files.insert(0, fileName)


        #### Dropdown menu updated
        self.UpdateOpenFileMenu()

        #### Manage open file history
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[self.u_info.max_num_recent_files:]

        settings.setValue('recentFileList', files)
        self.UpdateRecentFileMenu()


    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


    def ExitUniEm(self):  # wxGlade: ControlPanel.<event_handler>

        buttonReply = QMessageBox.question(self, 'Exit UNI-EM', "Do you exit UNI-EM?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if buttonReply == QMessageBox.No:
            return (0)
        elif buttonReply == QMessageBox.Yes:
            self.CloseAllFiles()
            sys.exit()


    def CloseAllFiles(self):
        for ofile in self.u_info.open_files4lock.values():
            if type(ofile) == dict :
                for ofileobj in ofile.values():
                    ofileobj.close()
            else :
                ofile.close()
        self.u_info.open_files4lock.clear()


    def CheckFileType(self, file_name):
        if os.path.isdir(file_name) :
            if self.CheckFolderDojo(file_name):
                filetype = "Dojo"
                return filetype
            ext = self.CheckFolderImage(file_name)
            if   len(ext) > 1 :
                filetype = "multiple type images"
            elif len(ext) == 1 :
                filetype = ext[0]
            else :
                filetype = "empty"
        else :
            filetype = "invalid"
            #
            # For future multipage tiff file
            #
            #root, ext = os.path.splitext(file_name)
            #if ext in ['.TIF','.tif', '.TIFF', '.tiff'] :
            #    filetype = "mtif"
            #else :
            #    filetype = "invalid"

        return filetype


    def CheckFolderImage(self, folder_path):
        filetypes = set()
        files_in_folder = glob.glob(os.path.join(folder_path, "*"))
        for file in files_in_folder:
            root, ext = os.path.splitext(file)
            if ext in ['.TIF','.tif', '.TIFF', '.tiff'] :
                filetypes.add('tif')
            if ext in ['.png','.PNG'] :
                filetypes.add('png')
            if ext in ['.jpg', '.jpeg'] :
                filetypes.add('jpg')
        return list(filetypes)

        tmp = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        input_files.extend(tmp)


    def CheckFolderDojo(self, folder_path):
        tmp_info = Params()
        tmp_info.SetUserInfo(folder_path)
        # Check file existence
        if  os.path.exists(tmp_info.files_path) and \
            os.path.exists(tmp_info.ids_path) and \
            os.path.exists(tmp_info.tile_ids_path) and \
            os.path.isfile(tmp_info.tile_ids_volume_file) and \
            os.path.isfile(tmp_info.color_map_file) and \
            os.path.isfile(tmp_info.segment_info_db_file) and \
            os.path.exists(tmp_info.images_path) and \
            os.path.exists(tmp_info.tile_images_path) and \
            os.path.isfile(tmp_info.tile_images_volume_file) :

            return 1
        else:
            return 0

