###
###
###
import sys, os

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(main_dir)
from miscellaneous.TabGenerator import TabGenerator

# ------------------------------------------------------------
# Example plugin
# Please modify this tab widget for your own use.
# Also edit Training.py and Inference.py
# ------------------------------------------------------------

plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
from plugins.Multicut.run_lifted_multicut   import LiftedMulticut
from plugins.Multicut.run_multicut  import Multicut


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
        tab = TabGenerator(self)

        # Training
        multicut        = Multicut(self.u_info)
        tab_multicut    = tab.GenerateTabWidget(multicut)
        tabs.addTab(tab_multicut, 'Multicut')

        # Inferernce
        lifted_multicut     = LiftedMulticut(self.u_info)
        tab_lifted_multicut = tab.GenerateTabWidget(lifted_multicut)
        tabs.addTab(tab_lifted_multicut, 'Lifted Multicut')

        # Show Widget
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()




