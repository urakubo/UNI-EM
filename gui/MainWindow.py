import sys
import os
import json
from  collections import OrderedDict
import importlib

from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, \
    qApp, QWidget, QHBoxLayout, QVBoxLayout, QLabel, \
    QPushButton, QAction, QMessageBox, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main

icon_dir            = path.join(main_dir, "icons")
icon_disabled_dir   = path.join(icon_dir, "Disabled")
plugins_dir         = path.join(main_dir, "plugins")
segmentation_dir    = path.join(main_dir, "segment")
annotator_dir       = path.join(main_dir, "annotator")

sys.path.append(path.join(main_dir, "plugins"))
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "plugins"))
sys.path.append(os.path.join(main_dir, "annotator"))

#
# For Pyinstaller
#
import annotator.Annotator.Annotator  as d1
import segment._2D_DNN._2D_DNN  as d2
import segment._3D_FFN._3D_FFN  as d3
import segment._tensorb._tensorb  as d4
import plugins.Blank.Blank  as d5
import plugins.Filter2D3D.Filter2D3D  as d6
import plugins.Template.Template  as d7
#

from Params  import Params
from Script  import Script
from DojoFileIO  import DojoFileIO
from FileMenu  import FileMenu
from DojoMenu  import DojoMenu
from Credit  import Credit
from func_persephonep import *

from miscellaneous.SyncListQComboBoxManager import *

class MainWindow(QMainWindow, FileMenu, DojoMenu, DojoFileIO, Credit, Script):

    def __del__(self):
        for ofile in self.u_info.open_files4lock.values():
            if type(ofile) == dict :
                for ofileobj in ofile.values():
                    ofileobj.close()
            else :
                ofile.close()
        self.u_info.open_files4lock.clear()


    def __init__(self):

        #
        # Define user info
        #
        self.u_info = Params()

        super(MainWindow, self).__init__()
        FileMenu.__init__(self)
        DojoMenu.__init__(self) # ???


        #
        # Prepare the main window
        #

        self.title = 'UNI-EM'
        self.left = 200
        self.top  = 200
        self.width = 1200
        self.height = 800

        SyncListQComboBoxExcludeDjojMtifManager.build(self.u_info)
        SyncListQComboBoxOnlyDojoManager.build(self.u_info)

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        main_menu = self.menuBar()

        ##
        ## File menu
        ##

        self.setAcceptDrops(True)
        file_menu = main_menu.addMenu('File')
        self.GenerateFileDropdownMenu( file_menu )


        ##
        ## Dojo menu
        ##

        dojo_folder = main_menu.addMenu('Dojo')
        self.dojo_icon_open_close = self.DojoDropdownMenu( dojo_folder )
        self.InitModeDojoMenu(self.dojo_icon_open_close)


        ##
        ## Annotator menu
        ##

        annotator_folder = main_menu.addMenu('Annotator')
        with open( path.join(annotator_dir, self.u_info.fname_menu) , 'r' ) as fp:
            e = json.load(fp, object_pairs_hook=OrderedDict)
        self.GenerateDropdownMenuToDialog(annotator_folder, e, 'annotator')


        ##
        ## Segmentation menu
        ##
        segmentation_folder = main_menu.addMenu('Segmentation')
        with open( path.join(segmentation_dir, self.u_info.fname_menu) , 'r' ) as fp:
            e = json.load(fp, object_pairs_hook=OrderedDict)
        self.GenerateDropdownMenuToDialog(segmentation_folder, e, 'segment')


        ##
        ## Plugin menu
        ##
        plugin_folder = main_menu.addMenu('Plugins')
        with open( path.join(plugins_dir, self.u_info.fname_menu) , 'r' ) as fp:
            e = json.load(fp, object_pairs_hook=OrderedDict)
        self.GenerateDropdownMenuToDialog(plugin_folder, e, 'plugins')


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

    # ----------------------------------------------------------------------

    def GenerateDropdownMenuToDialog(self, folder, e, target_folder):
        plugin_stack = [folder]
        snum_stack   = [0]
        items = e.items()
        # imported_module = {}
        for key, val in items:
            if val['Sub'] > 0:
                plugin_stack.append(QMenu(key, self))
                snum_stack = snum_stack + [ val['Sub'] ]
            else:
                id = QAction( key, self)
                modulename = val['Func']
                called_module= importlib.import_module(target_folder+'.'+ modulename+'.'+modulename)
                # imported_module[key] = called_module
                # print(call_module.__name__)
                id.triggered.connect( lambda  state, x = called_module: x.GenerateDialog(self) )
                plugin_stack[-1].addAction(id)
            while(len(plugin_stack) >= 2 and snum_stack[-1] <= 0):
                plugin_stack[-2].addMenu(plugin_stack[-1])
                plugin_stack.pop()
                snum_stack.pop()
            if snum_stack and (snum_stack[-1] > 0):
                snum_stack[-1] = snum_stack[-1] - 1
        # return imported_module

##
## Web browser
##

class PersephonepTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.parent = parent

        # initialize tab screen
        self.tabs = QTabWidget()
        self.tab = []  # Store the PersephonepWindow Class
        self.appl = []  # Store application ID
        self.tabs.resize(1200, 800)

        # define the delete tab process
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        #
        self.tabs.setUsesScrollButtons(True)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addTab(self, appl_id, title, url):
        ''' add Tab
        '''
        # print(index)
        # browser = PersephonepWindow(url)

        #
        # The following tab browser launch
        # (func_persephonep)
        # should generate a widget something like
        #
        # browser = PersephonepWindow(url)
        # widget = browser.Generate
        # self.tab.append(widget)
        #
        # The following is wrong.
        # The class object declaration (PersephonepWindow)
        # should not have any return.
        # but I keep it only for download indicator.
        # It should be revised in future.
        #
        self.tab.append(PersephonepWindow(url))
        self.appl.append(appl_id)
        self.tabs.addTab(self.tab[-1], '')  # do not match tab index & tab num
        # self.tabs.setTabText(index, title)
        # self.tabs.setCurrentIndex(index)
        self.tabs.setTabText(len(self.tab) - 1, title)
        self.tabs.setCurrentIndex(len(self.tab) - 1)
        # self.tab[-1].window.titleChanged.connect(self.updateTabName)

    def closeTab(self, index):
        ''' close Tab.
        '''
        ###
        if ('dojo' == self.appl[index]):
            flag = self.parent.CloseDojoFiles2()
            if (flag == 1):
                print('Error ocurred in closing Dojo.')
                return
        ###
        if ('annotator' == self.appl[index]):
            print('Close 3D Annotator')
            flag = self.parent.annotator.TerminateAnnotator()
            if (flag == 1):
                print('Error ocurred in closing annotator.')
                return
        ###
        if ('tensorboard' == self.appl[index]):
            flag = self.parent.process_tensorboard.terminate()
            if (flag == 1):
                print('Error ocurred in closing tensorboard.')
                return
        ###
        self.tab.pop(index)
        # appl = self.appl.pop(index)
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


###

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


