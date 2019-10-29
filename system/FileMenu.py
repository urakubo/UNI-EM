
import sys
import os
from os import path, pardir
from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QPoint


main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")
sys.path.append(os.path.join(main_dir, "system"))
sys.path.append(os.path.join(main_dir, "dojoio"))

from FileManager  import FileManager

class FileMenu(FileManager):
    def __init__(self):
        # File menu
        self.file_menu = ['Open Image/Dojo Folder',
                          'Open Multipage Tiff File',
                          'Create Dojo Folder',
                          'Open Recent File/Folder',
                          'Exit from UNI-EM']
        self.file_icon = ['Folder_Open_16.png',
                          'Photo_Open_16.png',
                          'Photo_Import_16.png',
                          'Search_16.png',
                          'Power_Off_16.png']
        self.file_action = [self.OpenFolder,
                          self.OpenMultiTiffFile,
                          self.GenerateDojoFolder,
                          self.Dummy,
                          self.ExitUniEm]

        self.menu_open_files   = []
        self.menu_recent_files = []



    def ContextMenu(self, point):
        activeAction = self.local_file_menu.activeAction()
        if not activeAction:
            return
        else:
            if activeAction.text() in self.file_menu:
                return

        menu = QMenu(self.local_file_menu)
        menu.setStyleSheet("background-color:white;")
        menu.setStyleSheet("color:black;")

        action = QAction('Close', self)
        action.triggered.connect(lambda e: self.CloseFileFolder(activeAction))
        menu.addAction(action)
        
        menu.exec_(self.local_file_menu.mapToGlobal(point))



    def GenerateFileDropdownMenu(self, file_menu):

        ## Prepare recent files/folders
        for i in range(self.u_info.max_num_recent_files):
            self.menu_recent_files.append(
            QAction(self, visible=False,
            	triggered=self.OpenRecentFileFolder))

        ## Prepare opend files/folders
        for i in range(self.u_info.max_num_open_files):
            self.menu_open_files.append(
            QAction(self, visible=False,
            	triggered=self.Dummy))


        self.local_file_menu = file_menu

        file_menu.setContextMenuPolicy(Qt.CustomContextMenu)
        file_menu.customContextMenuRequested.connect(self.ContextMenu)

        ##
        ## File menu
        ##

        ## "Open Image/Dojo Folder"
        id = self.MakeMenuItem(0)
        file_menu.addAction(id)


        #
        # For future release
        #
        ## "Open Multipage Tiff File"
        #id = self.MakeMenuItem(1)
        #file_menu.addAction(id)


        ## Generate Dojo Folder
        id = self.MakeMenuItem(2)
        file_menu.addAction(id)


        ## "Open Recent File/Folder"
        submenu = QMenu(self.file_menu[3], self)
        file_menu.addMenu(submenu)
        for i in range(self.u_info.max_num_recent_files):
            submenu.addAction(self.menu_recent_files[i])

        self.UpdateRecentFileMenu()

        ## Opened files/folders
        self.separator1 = file_menu.addSeparator()
        self.separator1.setVisible(False)
        myfont=QFont("Courier")
        myfont.setBold(True)
        myfont.setPointSize(9)
        self.separator_title = QAction('Open', self)
        self.separator_title.setFont(myfont)
        self.separator_title.setVisible(False)
        file_menu.addAction(self.separator_title)
        for i in range(self.u_info.max_num_open_files):
            file_menu.addAction(self.menu_open_files[i])
        self.separator2 = file_menu.addSeparator()
        self.separator2.setVisible(False)


        ## "Exit from UNI-EM"
        id = self.MakeMenuItem(4)
        file_menu.addAction(id)



    def MakeMenuItem(self, i):
        ii = QIcon()
        ii.addPixmap(QPixmap(path.join(icon_dir, self.file_icon[i])), QIcon.Normal, QIcon.On)
        id = QAction(ii, self.file_menu[i], self)
        id.triggered.connect(self.file_action[i])
        return id

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 
    
    def dropEvent(self, event):
        files = [str(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            print('Dropfile: ', f)
            self.OpenDropdownFileFolder(f)


# For future release
#
