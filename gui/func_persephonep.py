#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from time import sleep
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFileDialog, QProgressBar,
                              QTextEdit, QGridLayout, QApplication, QPushButton,  QDesktopWidget)

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem, QWebEnginePage
from PyQt5 import QtNetwork

__program__ = 'PERSEPHONEP'


PROGRESS_STYLE = """
QProgressBar {
    background-color: white;
    text-align: center;
    height: 20px;
}
QProgressBar::chunk {
    background-color: #01DF74;
    margin: 1px;
    width: 10px;
    height: 20px;
}
"""

''' This is a single page of the browser.
    This class equals a tab of PersephonepTableWidget.
    This class can run only this python script, however,
    that is not recomended.
    (This ability might be deleted in the near future.)
'''
class PersephonepWindow(QWidget):
    
    def __init__(self):
        super(PersephonepWindow, self).__init__()

    def Generate(self, url):

        self.initurl = url

        # config
        # initurl = 'https://www.google.co.jp'
        
        # setting window
        self.window = QWebEngineView()

        proxy = QtNetwork.QNetworkProxy()
        proxy.setType(QtNetwork.QNetworkProxy.NoProxy)
        #proxy.setHostName("10.232.11.28")
        #proxy.setPort(6666)
        QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
   
        # condig url
        ###self.window.load(QUrl(self.initurl))
        self.window.load(QtCore.QUrl(self.initurl))
        #self.window.resize(1000,600)
        #self.window.move(200,200)
        #self.window.setWindowTitle(__program__)

        # setting button
        #self.back_button = QPushButton('back')
        #self.back_button.setToolTip('Go back to previous page.')
        #self.back_button.clicked.connect(self.window.back)
        #self.forward_button = QPushButton('forward')
        #self.forward_button.setToolTip('Go to the next page.')
        #self.forward_button.clicked.connect(self.window.forward)
        self.reload_button = QPushButton('reload')
        self.reload_button.setToolTip('Reload this page.')
        self.reload_button.clicked.connect(self.window.reload)


        ##
        ## Download dialog
        ##
        self.progress = QProgressBar(self)
        self.progress.setMaximum(100)
        self.progress.setStyleSheet(PROGRESS_STYLE)
        self.progress.hide()
        self.downloading_filename = ''
        ##
        ##

        self.url_edit = QLineEdit()
        self.url_edit.setText( self.initurl )
        self.url_edit.setReadOnly(True)
        #self.url_edit.setEnabled(False)
        self.url_edit.setToolTip('URL box')
        #self.move_button = QPushButton('move')
        #self.move_button.setToolTip('Move to the page set at URL box.')
        #self.move_button.clicked.connect(self.loadPage)
        #self.url_edit.returnPressed.connect(self.loadPage)
        self.home_button = QPushButton('home')
        self.home_button.setToolTip('Move to the home page.')
        self.home_button.clicked.connect(self.loadHomePage)
        
        # signal catch from moving web pages.


        ##
        ## Download dialog
        ##
        self.window.urlChanged.connect(self.updateCurrentUrl)
        # self.window.page().profile().downloadRequested.connect(self._downloadRequested)
        self.window.page().profile().downloadRequested.connect(self.on_download_requested)
        ##


        # setting layout
        tab = QWidget()
        tab.layout = QGridLayout(tab)
        tab.layout.setSpacing(0)
        #grid.addWidget(self.back_button, 1, 0)
        #grid.addWidget(self.forward_button, 1, 1)
        tab.layout.addWidget(self.reload_button, 1, 2)
        tab.layout.addWidget(self.url_edit, 1, 3, 1, 10)
        #grid.addWidget(self.move_button, 1, 14)
        #grid.addWidget(self.home_button, 1, 15)
        tab.layout.addWidget(self.window,2, 0, 5, 16)
        tab.layout.addWidget(self.progress, 7, 0, 1, 3) #### Download
        tab.setLayout(tab.layout)
        return tab

    
    def center(self):
        ''' centering widget
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check_url_protocol(self, move_url):
        if (move_url[0:7] == 'http://' or
            move_url[0:8] == "https://" or
            move_url[0:8] == 'file:///' or
            move_url[0:6] == 'ftp://'):
            return True
        else:
            return False
        

    def check_url_protocol_ipv4(self, move_url):
        ''' return True if move_url is IPv4 using Regular expression
        '''
        return re.match('(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])', move_url)
        
    
    def updateCurrentUrl(self):
        ''' rewriting url_edit when you move different web page.
        '''
        # current_url = self.window.url().toString()
        self.url_edit.clear()
        self.url_edit.insert(self.window.url().toString())
        
    
    def loadHomePage(self):
        ''' move to the home page
        '''
        #initurl = 'https://www.google.co.jp'
        #self.window.load(QUrl(initurl))
        self.window.load(QtCore.QUrl(initurl)) ### Download

    def saveFile(self):
        print('download')


    @QtCore.pyqtSlot(QWebEngineDownloadItem)
    def on_download_requested(self, download):
        #print('{} downloading to {}'.format(download.url(), download.path()))
        self.downloading_filename = QtCore.QFileInfo(download.path()).fileName()
        self.progress.setValue(0)
        self.progress.show()
        download.downloadProgress.connect(self.on_download_progress)
        download.stateChanged.connect(self.on_download_state)
        download.accept()


    def on_download_progress(self, read, total):
        self.progress.setValue((total/read)*100)
        self.progress.setFormat('{} : {}%'.format(self.downloading_filename, (total/read)*100))

    def on_download_state(self, state):
        if state == QWebEngineDownloadItem.DownloadRequested:
            print('requested')
        elif state == QWebEngineDownloadItem.DownloadInProgress:
            print('progress')
        elif state == QWebEngineDownloadItem.DownloadCompleted:
            print('Download complete')
            sleep(1)    ################ Download
            self.progress.hide()
        elif state == QWebEngineDownloadItem.DownloadCancelled:
            print('cancel')
        elif state == QWebEngineDownloadItem.DownloadInterrupted:
            print('interrupt')





if __name__ == '__main__':
    # mainPyQt5()
    app = QApplication(sys.argv)

    # setWindowIcon is a method for QApplication, not for QWidget
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon_persephone.png')
    app.setWindowIcon(QIcon(path))

    ex = PersephonepWindow()
    sys.exit(app.exec_())
            
    
    
