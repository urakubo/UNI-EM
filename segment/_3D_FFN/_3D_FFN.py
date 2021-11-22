###
###
###

import sys, os, time, errno

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
from miscellaneous.TabGenerator import TabGenerator

icon_dir = path.join(main_dir, "icons")
_3D_FFN_dir = path.join(main_dir, "segment",'_3D_FFN')
sys.path.append(_3D_FFN_dir)
from segment._3D_FFN.FFNPrepTraining   import FFNPrepTraining
from segment._3D_FFN.FFNTraining    import FFNTraining
from segment._3D_FFN.FFNInference   import FFNInference
from segment._3D_FFN.FFNPostprocessing   import FFNPostprocessing
from segment._3D_FFN.FFNConsensus   import FFNConsensus

segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)


class GenerateDialog(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "3D FFN"
        self.initUI()


    def initUI(self):
        ##
        ## Define tab
        ##
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.resize(300, 500)
        tab  = TabGenerator(self)

        ##
        ## FFN preparation
        ##
        prep_ffn = FFNPrepTraining(self.u_info)
        Widget1_bottom = tab.GenerateTabWidget(prep_ffn) # Widget
        tabs.addTab(Widget1_bottom, 'Preprocessing')

        ##
        ## FFN training
        ##
        run_ffn = FFNTraining(self.u_info)
        Widget2_bottom = tab.GenerateTabWidget(run_ffn) # Widget
        tabs.addTab(Widget2_bottom, 'Training')

        ##
        ## FFN inferernce
        ##
        run_ffn = FFNInference(self.u_info)
        Widget3_bottom = tab.GenerateTabWidget(run_ffn) # Widget
        tabs.addTab(Widget3_bottom, 'Inference')

        ##
        ## FFN postprocessing
        ##
        run_ffn = FFNPostprocessing(self.u_info)
        Widget4_bottom = tab.GenerateTabWidget(run_ffn) # Widget
        tabs.addTab(Widget4_bottom, 'Postprocessing')


        ##
        ## FFN concensus
        ##
        run_ffn = FFNConsensus(self.u_info)
        Widget5_bottom = tab.GenerateTabWidget(run_ffn) # Widget
        tabs.addTab(Widget5_bottom, 'Consensus')

        ##
        ## Generate tabs
        ##

        layout.addWidget(tabs)
        self.setLayout(layout)


        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()

    ##
