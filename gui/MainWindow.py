
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import json
from  collections import OrderedDict

from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, qApp, QWidget, QHBoxLayout, QVBoxLayout, QLabel, \
    QPushButton, QAction, QMessageBox, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")
sys.path.append(path.join(main_dir, "plugins"))
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "plugins"))
plugins_dir = path.join(main_dir, "plugins")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(os.path.join(main_dir, "annotator"))
annotator_dir = path.join(main_dir, "annotator")


from Params  import Params
from Script  import Script
from Annotator import Annotator
from Plugins import Plugins
from Segment import Segment
from FileIO  import FileIO

from FileMenu  import FileMenu
from Credit  import Credit
from ExportImageDialog import ExportImageDialog
from ExportIdDialog import ExportIdDialog
from func_persephonep import *

class MainWindow(QMainWindow, FileMenu, Credit, Annotator, Plugins, Segment, FileIO, Script):
# class MainWindow(QMainWindow, Credit, Plugins):

    def __init__(self):

        #
        # Define user info
        #
        self.u_info = Params()

        #
        # Prepare the main window
        #
        super().__init__()
        self.title = 'UNI-EM'
        self.left = 200
        self.top  = 200
        self.width = 1200
        self.height = 800

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        main_menu = self.menuBar()

        ##
        ## File menu
        ##

        file_folder = main_menu.addMenu('Dojo')
        self.file_id = self.InitialzeFileMenu( file_folder )
        self.InitModeFileMenu(self.file_id)


        ##
        ## Annotator menu
        ##

        annotator_folder = main_menu.addMenu('Annotator')

        # Parse the json file "plugin/menu.json"
        with open( path.join(annotator_dir, self.u_info.fname_menu) , 'r' ) as fp:
            e = json.load(fp, object_pairs_hook=OrderedDict)
        annotator_stack = [annotator_folder]
        snum_stack   = [0]
        items = e.items()    # python3

        for key, val in items:
            if val['Sub'] > 0:
                annotator_stack.append(QMenu(key, self))
                snum_stack = snum_stack + [ val['Sub'] ]
            else:
                id = QAction( key, self)
                id.triggered.connect( getattr(self, val['Func']) )
                annotator_stack[-1].addAction(id)
            while(len(annotator_stack) >= 2 and snum_stack[-1] <= 0):
                annotator_stack[-2].addMenu(annotator_stack[-1])
                annotator_stack.pop()
                snum_stack.pop()
            if snum_stack and (snum_stack[-1] > 0):
                snum_stack[-1] = snum_stack[-1] - 1




        ##
        ## Segmentation menu
        ##

        segmentation_folder = main_menu.addMenu('Segmentation')

        # Parse the json file "plugin/menu.json"
        with open( path.join(segmentation_dir, self.u_info.fname_menu) , 'r' ) as fp:
            e = json.load(fp, object_pairs_hook=OrderedDict)
        segmentation_stack = [segmentation_folder]
        snum_stack   = [0]
        items = e.items()    # python3

        for key, val in items:
            if val['Sub'] > 0:
                segmentation_stack.append(QMenu(key, self))
                snum_stack = snum_stack + [ val['Sub'] ]
            else:
                id = QAction( key, self)
                id.triggered.connect( getattr(self, val['Func']) )
                segmentation_stack[-1].addAction(id)
            while(len(segmentation_stack) >= 2 and snum_stack[-1] <= 0):
                segmentation_stack[-2].addMenu(segmentation_stack[-1])
                segmentation_stack.pop()
                snum_stack.pop()
            if snum_stack and (snum_stack[-1] > 0):
                snum_stack[-1] = snum_stack[-1] - 1

        ##
        ## Plugin menu
        ##

        plugin_folder = main_menu.addMenu('Plugins')

        # Parse the json file "plugin/menu.json"
        with open( path.join(plugins_dir, self.u_info.fname_menu) , 'r' ) as fp:
            e = json.load(fp, object_pairs_hook=OrderedDict)
        plugin_stack = [plugin_folder]
        snum_stack   = [0]
        items = e.items()    # python3

        for key, val in items:
            if val['Sub'] > 0:
                plugin_stack.append(QMenu(key, self))
                snum_stack = snum_stack + [ val['Sub'] ]
            else:
                id = QAction( key, self)
                id.triggered.connect( getattr(self, val['Func']) )
                plugin_stack[-1].addAction(id)
            while(len(plugin_stack) >= 2 and snum_stack[-1] <= 0):
                plugin_stack[-2].addMenu(plugin_stack[-1])
                plugin_stack.pop()
                snum_stack.pop()
            if snum_stack and (snum_stack[-1] > 0):
                snum_stack[-1] = snum_stack[-1] - 1



        ##
        ## Script menu
        ##

        help_id  = QAction('Run Script', self)
        help_id.triggered.connect(self.Script)

        help_folder = main_menu.addMenu('Script')
        help_folder.addAction(help_id)


        ##
        ## Help menu
        ##

        help_id  = QAction('About UNI-EM', self)
        help_id.triggered.connect(self.Credit)

        help_folder = main_menu.addMenu('Help')
        help_folder.addAction(help_id)

        ##
        ## Web browser
        ##

        self.table_widget = PersephonepTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class PersephonepTableWidget(QWidget):

        def __init__(self, parent):
            super(QWidget, self).__init__(parent)
            self.layout = QVBoxLayout(self)
            self.parent = parent

            # initialize tab screen
            self.tabs = QTabWidget()
            self.tab  = [] # Store the PersephonepWindow Class
            self.appl = [] # Store application ID
            self.tabs.resize(1200, 800)

            # Add Tabs
            # self._addTab(len(self.tab),'Google')  # len(self.tab) => 0

            # self.add_button = QPushButton('+')
            # self.add_button.setStyleSheet('background-color:gray')
            # self.add_button.clicked.connect(lambda: self._addTab(len(self.tab)))  # add tab to last of index


            # define the delete tab process
            self.tabs.setTabsClosable(True)
            self.tabs.tabCloseRequested.connect(self.closeTab)

            #
            self.tabs.setUsesScrollButtons(True)
            ########## Create first tab
            # self.tab[0].layout = QVBoxLayout(self)
            # self.pushButton1 = QPushButton('PyQt5 button')
            # self.tab[0].layout.addWidget(self.pushButton1)
            # self.tab[0].setLayout(self.tab[0].layout)

            # Add tabs to widget
            # self.layout.addWidget(self.add_button)
            self.layout.addWidget(self.tabs)

            # self.app_info = QLabel( 'This is a Web Browser based on Python 3 and PyQt5.' )
            # self.layout.addWidget(self.app_info)
            self.setLayout(self.layout)


        def addTab(self, appl_id, title, url):
            ''' add Tab
            '''
            # print(index)
            self.tab.append(PersephonepWindow( url, parent=self ))
            self.appl.append(appl_id)
            self.tabs.addTab(self.tab[-1], '')  # do not match tab index & tab num
            # self.tabs.setTabText(index, title)
            # self.tabs.setCurrentIndex(index)
            self.tabs.setTabText(len(self.tab)-1, title)
            self.tabs.setCurrentIndex(len(self.tab)-1)
            #self.tab[-1].window.titleChanged.connect(self.updateTabName)


        def closeTab(self, index):
            ''' close Tab.
            '''
            ###
            if ('dojo' == self.appl[index]):
                fail = self.parent.CloseDojoFiles2()
                if (fail == 1):
                    return
            ###
            if ('annotator' == self.appl[index]):
                fail = self.parent.CloseStlViewer()
                if (fail == 1):
                    return
            ###
            self.tab.pop(index)
            appl = self.appl.pop(index)
            self.tabs.removeTab(index)

        def updateTabName(self):
            ''' re-set tab name
            '''
            self.tabs.setTabText(self.tabs.currentIndex(), self.tab[self.tabs.currentIndex()].window.title())

        def center(self):
            ''' centering widget
            '''
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

        @pyqtSlot()
        def on_click(self):
            print("\n")
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


