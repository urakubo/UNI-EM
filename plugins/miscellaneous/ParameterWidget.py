from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from .Widget import Widget

class ParameterWidget(QVBoxLayout):
    def __init__(self):
        super(ParameterWidget,self).__init__()

        self.width = 150
        self.height = 150
        self.widgets = []

        bold = QFont()
        bold.setBold(True)

        self.title = QLabel('Parameter')
        self.title.setFont(bold)
        self.title.setMinimumWidth(self.width)
        self.setTitle('')
        self.setAlignment(Qt.AlignBottom)
        self.addWidget(self.title, False)

    def setTitle(self, text):
        self.title.setText(text)

    def addWidget(self, w, isManage=True):
        super(ParameterWidget, self).addWidget(w)
 
        if isManage:
            self.widgets.append(w)

    def remove(self):
        for w in self.widgets:
            w.deleteLater()
        self.widgets = []

