from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, QSlider, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, \
    QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSlot


import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class CanvasLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(CanvasLabel, self).__init__(*args, **kwargs)
        self.mousePressEvent = self.onMousePress
        self.mouseMoveEvent = self.onMouseMove
        self.changePosCallback = None

        self.baseX = 0
        self.baseY = 0

    def onMousePress(self, e):
        x = e.pos().x()
        y = e.pos().y() 

        self.baseX = x
        self.baseY = y 

    def onMouseMove(self, e):
        x = e.pos().x()
        y = e.pos().y() 
        
        if self.changePosCallback is not None:
            relativeX = x - self.baseX
            relativeY = y - self.baseY
            self.changePosCallback(-1 * relativeX, -1 * relativeY)

        self.baseX = x
        self.baseY = y 

