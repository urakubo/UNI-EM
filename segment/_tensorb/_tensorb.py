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


class GenerateDialog(QWidget):
    def __init__(self, parent):
        self.u_info = parent.u_info
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):

        ## Dialog: Is Tensorboard already launched?
        #print(self.parent.table_widget.appl)
        if 'tensorboard' in self.parent.table_widget.appl:
            QMessageBox.information(self, "Tensorboard", "Tensorboard has already been launched!")
            return

        ## Select Tensorboard Folder
        newdir = QFileDialog.getExistingDirectory( self, "Select tensorboard folder", self.u_info.data_path )
        if len(newdir) == 0:
            print('No folder was selected.')
            return

        ## Tensorboard launch.
        self.StartTensorboard(newdir)


    def StartTensorboard(self, newdir):

        tmp = [ \
        		'--logdir'		, newdir				, \
				'--host'		, socket.gethostbyname(socket.gethostname()) ]
        comm = self.u_info.exec_tensorboard[:]
        comm.extend( tmp )

        print(comm)

        try:
            self.parent.process_tensorboard = s.Popen(comm, stdout=s.PIPE)
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



