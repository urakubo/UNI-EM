###
###
###
import sys, os, time, errno, copy, fnmatch
#from lockfile import LockFile
#import portalocker

from os import path, pardir
import glob
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "system"))
sys.path.append(os.path.join(main_dir, "dojoio"))

from DialogGenerateDojoFolder import DialogGenerateDojoFolder

#from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt
from PyQt5.QtWidgets import (QFileDialog, qApp, QMessageBox)
from Params import Params

from miscellaneous.SyncListQComboBoxManager import *
import miscellaneous.Miscellaneous as m

class FileManager():

    def GenerateDojoFolder(self):
        tmp = DialogGenerateDojoFolder(self, self.u_info)

    def OpenRecentFileFolder(self):
        action = self.sender()
        if not action:
            return
        file_name  = action.data()
        if not os.path.exists( file_name ):
            QMessageBox.warning(self, "Recent Files",
                                "Cannot find file: %s" % file_name)
            return
        return self.OpenFolder( file_name )


    def OpenDropdownFileFolder(self, file_name):
        return self.OpenFolder( file_name )


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
        file_name = activeAction.data()
        self.ExecuteCloseFileFolder(file_name)

    def ExecuteCloseFileFolder(self, file_name):
        if os.path.isdir(file_name):
            m.UnlockFolder(self.u_info, file_name)
        else:
            self.u_info.open_files4lock[file_name].close()
            del self.u_info.open_files4lock[file_name]

        self.u_info.open_files.remove(file_name)
        self.UpdateOpenFileMenu()

        SyncListQComboBoxEmptyManager.get().removeModel(file_name)
        SyncListQComboBoxFFNsManager.get().removeModel(file_name)
        SyncListQComboBoxModelManager.get().removeModel(file_name)
        SyncListQComboBoxEmptyModelManager.get().removeModel(file_name)
        SyncListQComboBoxImageManager.get().removeModel(file_name)
        SyncListQComboBoxDojoManager.get().removeModel(file_name)
        SyncListQComboBoxSplitterManager.get().removeModel(file_name)

######

##
# try:
#    self.u_info.open_files4lock[fileName] = open(fileName, 'r+')
# except:
#    print("Cannot open file.")
#    return  False
##


    def OpenDialogOpenFolder(self):
        initdir = os.path.normpath( path.join(main_dir, "..") )
        open_folder_name = QFileDialog.getExistingDirectory(self, "Select folder (Dojo/Image/Model/Empty)", initdir)
        if len(open_folder_name) == 0:
            print('No folder was selected.')
            return
        open_folder_name = open_folder_name.replace('/', os.sep)
        flag = self.OpenFolder(open_folder_name)
        return flag


    def OpenFolder(self, file_folder_name):

        print('file_folder_name: ', file_folder_name)
        if self.InitialCheckOpenFolder(file_folder_name) == False:
            return False

        folder_type = self.CheckFolderType(file_folder_name)
        if folder_type == False :
            return False
        print('Folder type: ', folder_type)
        flag = self.ExecuteFolderOpen(file_folder_name, folder_type)
        if flag == False :
            return False
        self.AddDropDownMenu( file_folder_name )
        return True


    def OpenSpecificFolder(self, folder_name, required_folder_types):

        if self.InitialCheckOpenFolder(folder_name) == False:
            return False

        folder_type = self.CheckFolderType(folder_name)
        if folder_type == False :
            return False
        elif folder_type not in required_folder_types :
            print( 'Not a required folder type: ', required_folder_types )
        else :
            print( 'Folder type: ', folder_type)

        return self.ExecuteFolderOpen(folder_name, folder_type)


    def CheckFolderType(self, folder_name):

        if self.CheckFolderDojo(folder_name):
            return "Dojo"
        elif self.CheckFolderModelTensorflow(folder_name):
            return "Model"
        elif self.CheckFolderFFNs(folder_name):
            return "FFNs"
        elif self.CheckFolderSplitterMerger(folder_name):
            return "Split"
        elif self.CheckFolderImage(folder_name) != [] :
            ext = self.CheckFolderImage(folder_name)
            if   len(ext) > 1 :
                filetype = "multiple type images"
                print('We do not accpet the Folder contains multiple image types.')
                return False
            else :
                return ext[0]
        else : 
            return "Empty"
        return False


    def InitialCheckOpenFolder(self,folder_name):

        if not os.path.isdir(folder_name) :
            print('Curently, we do not accpet files, but only folders.')
            return False
        if folder_name in self.u_info.open_files:
            print('Already open.')
            return False
        elif len(self.u_info.open_files) >= self.u_info.max_num_open_files :
            print('Exceeding the maximal number of open folders: ', self.u_info.max_num_open_files)
            return False


    def AddDropDownMenu(self, folder_name):

        ## Dropdown menu updated
        self.UpdateOpenFileMenu()
        SyncListQComboBoxEmptyManager.get().addModel(folder_name)
        SyncListQComboBoxFFNsManager.get().addModel(folder_name)
        SyncListQComboBoxModelManager.get().addModel(folder_name)
        SyncListQComboBoxEmptyModelManager.get().addModel(folder_name)
        SyncListQComboBoxImageManager.get().addModel(folder_name)
        SyncListQComboBoxDojoManager.get().addModel(folder_name)
        SyncListQComboBoxSplitterManager.get().addModel(folder_name)


    def ExecuteFolderOpen(self, folder_name, folder_type):

        ## Folder open
        lock_result = m.LockFolder(self.u_info, folder_name)
        if lock_result == False:
            return False
        self.u_info.open_files_type[folder_name] = folder_type
        self.u_info.open_files.insert(0, folder_name)

        ## Manage open file history
        settings = QSettings('Trolltech', 'Recent Files Example')
        recent_files = settings.value('recentFileList', [])

        try:
            recent_files.remove(folder_name)
        except ValueError:
            pass

        recent_files.insert(0, folder_name)
        del recent_files[self.u_info.max_num_recent_files:]

        settings.setValue('recentFileList', recent_files)
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


    def CheckFolderImage(self, folder_path):
        filetypes = set()
        files_in_folder = glob.glob(os.path.join(folder_path, "*"))
        for file in files_in_folder:
            root, ext = os.path.splitext(file)
            if ext in ['.TIF','.tif', '.TIFF', '.tiff'] :
                filetypes.add('tif')
            if ext in ['.png','.PNG'] :
                filetypes.add('png')
            if ext in ['.jpg', '.jpeg','.JPG', '.JPEG'] :
                filetypes.add('jpg')
        return list(filetypes)


    def CheckFolderDojo(self, folder_path):
        tmp_info = Params()
#        tmp_info = copy.copy(self.u_info)
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


    def CheckFolderSplitterMerger(self, folder_path):
        required_files = [ \
            'attr.json', \
            'img', \
            'seg']
        tmp = glob.glob( path.join(folder_path, "*") )
        filenames_in_folder = [os.path.basename(r) for r in tmp]

        flags = []
        for required_file in required_files:
            match_fname = [fnmatch.fnmatch(fn, required_file) for fn in filenames_in_folder]
            flags.append(any(match_fname))
        if all(flags):
            return 1
        else:
            return 0


    def CheckFolderModelTensorflow(self, folder_path):

        required_files = [ \
            'model*.meta', \
            'model*.index',\
            'model*.data-00000-of-00001' ]
        tmp = glob.glob( path.join(folder_path, "*") )
        filenames_in_folder = [os.path.basename(r) for r in tmp]
        # print('filenames_in_folder : ',filenames_in_folder)
		#
        cropped = []
        for required_file in required_files:
			#
            tmp = fnmatch.filter(filenames_in_folder, required_file)
            if len(tmp) == 0:
                return 0
			#
            a, b = map(len, required_file.split('*'))
            cropped.append( {t[a:-b] for t in tmp} ) 
        intersection = cropped[0] & cropped[1] & cropped[2] 
        # print('intersection : ' , intersection) 
        return (len(intersection) > 0)


    def CheckFolderFFNs(self, folder_path):

        required_files = [ \
            'af.h5', \
            'grayscale_maps.h5', \
            'groundtruth.h5', \
            'tf_record_file' ]
        tmp = glob.glob( path.join(folder_path, "*") )
        filenames_in_folder = [os.path.basename(r) for r in tmp]

        flags = []
        for required_file in required_files:
            match_fname = [fnmatch.fnmatch(fn, required_file) for fn in filenames_in_folder]
            flags.append(any(match_fname))
        if all(flags):
            return 1
        else:
            return 0


    def OpenMultiTiffFile(self):
        initdir = os.path.normpath( path.join(main_dir, "..") )
        tiff_file = QFileDialog.getOpenFileName(self, "Select Multipage Tiff File", initdir, "TIFF (*.TIF *.tif *.TIFF *.tiff)")
        tiff_file = tiff_file[0]
        if len(tiff_file) == 0:
            return False
        tiff_file = tiff_file.replace('/', os.sep)
        self.OpenFileFolder(tiff_file)
