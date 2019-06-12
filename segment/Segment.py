
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

import socket
import sys
import os
import subprocess as s
import time
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)


# ----------------------------------------------------------------------
# Interface of plugins to Control Panel
# Please add user defined functions
# Also please edit "menu.json" for a plugins pulldown menu.
# ----------------------------------------------------------------------

sys.path.append(path.join(segmentation_dir, "_2D_DNN"))
sys.path.append(path.join(segmentation_dir, "_3D_FFN"))

from Dialog_2D_DNN import Dialog_2D_DNN
from Dialog_3D_FFN import Dialog_3D_FFN


class Segment():

    def _2D_DNN(self):
        self.tmp = Dialog_2D_DNN(self)

    def _3D_FFN(self):
        self.tmp = Dialog_3D_FFN(self)

    def _Tensorboard(self):

        ## Dialog: Is Tensorboard already launched?
        if 1 in self.table_widget.appl:
            QMessageBox.information(self, "Tensorboard", "Tensorboard has already been launched!")
            return

        ## Select Tensorboard Folder
        newdir = QFileDialog.getExistingDirectory(self, "Select tensorboard folder", self.u_info.tensorflow_model_path)
        if len(newdir) == 0:
            print('No folder was selected.')
            return
        self.u_info.tensorboard_path = newdir

        ## Tensorboard launch.
        self.StartTensorboard()


    def StartTensorboard(self):

        comm = self.u_info.exec_tensorboard   + ' ' \
                + ' --logdir ' + self.u_info.tensorboard_path + ' ' \
                + ' --host ' + socket.gethostbyname(socket.gethostname())
        try:
            self.p = s.Popen(comm.split(), stdout=s.PIPE)
            time.sleep(1)
            self.table_widget.addTab('tensorboard', 'Tensorboard',
                                     'http://' + socket.gethostbyname(socket.gethostname()) + ':6006')
            print("Start tensorboard")
            return
        except s.CalledProcessError as e:
            print("Error ocurrs in tensorboard")
            return

    def CloseTensorboard(self):
        self.p.terminate()
        print("Stop tensorboard")



# ----------------------------------------------------------------------

