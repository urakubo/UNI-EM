###
###
###
import sys, os


from PyQt5.QtWidgets import  QMessageBox,  QWidget, QFileDialog
import subprocess as s
import socket
import time

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)

#
class dummy():
    def __init__(self):
        pass


class GenerateDialog(QWidget):
    def __init__(self, parent):
        self.u_info = parent.u_info
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):

        ## Dialog: Is Tensorboard already launched?
        if 1 in self.parent.table_widget.appl:
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
            self.parent.process_tensorboard = s.Popen(comm.split(), stdout=s.PIPE)
            time.sleep(1)
            self.parent.table_widget.addTab('tensorboard', 'Tensorboard',
                                     'http://' + socket.gethostbyname(socket.gethostname()) + ':6006')
            print("Start tensorboard")
            return
        except s.CalledProcessError as e:
            print("Error ocurrs in tensorboard")
            return

#    def CloseTensorboard(self):
#        self.p.terminate()
#        print("Stop tensorboard")



