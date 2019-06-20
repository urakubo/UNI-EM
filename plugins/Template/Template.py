###
###
###
import sys, os

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")

from miscellaneous.TabTemplate import TabTemplate

# ------------------------------------------------------------
# Example plugin
# Please modify this tab widget for your own use.
# Also edit Training.py and Inference.py
# ------------------------------------------------------------

plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
from plugins.Template.Training   import Training
from plugins.Template.Inference  import Inference


class dummy():
    def __init__(self):
        pass

class GenerateDialog(QWidget):
    def __init__(self, parent):
        self.title  = "Template"
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.u_info = parent.u_info
        self.parent = parent
        super().__init__()
        self.initUI()


    def initUI(self):

        # Generate tab
        tabs   = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)
        tab = TabTemplate(self)

        # Training
        training        = Training(self.u_info)
        tab_training    = tab.GenerateTabWidget(training)
        tabs.addTab(tab_training, 'Training')

        # Inferernce
        inference        = Inference(self.u_info)
        tab_inference    = tab.GenerateTabWidget(inference)
        tabs.addTab(tab_inference, 'Inference')

        # Show Widget
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()




