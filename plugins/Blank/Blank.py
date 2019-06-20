###
###
###
import sys, os


from PyQt5.QtWidgets import  QMessageBox,  QWidget
from PyQt5.QtGui import QIcon, QPixmap

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
#
class dummy():
    def __init__(self):
        pass


class GenerateDialog(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initUI()

    def initUI(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Blank")
        msgBox.setText("This is blank!")
        msgBox.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        returnValue = msgBox.exec()
        return False

