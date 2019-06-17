###
###
###
import sys, os


from PyQt5.QtWidgets import  QMessageBox,  QWidget


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)

#
class GenerateDialog(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initUI()

    def initUI(self):

        QMessageBox.information(self, "Blank", "This is blank!")
        return False

