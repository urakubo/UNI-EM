###
###
###

import sys, os, time, errno

import numpy as np
import copy
from itertools import chain
import subprocess as s
import time


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "filesystem"))

##
##

from MiscellaneousSegment import MiscellaneousSegment

if getattr(sys, 'frozen', False):
    exec_run_translate = os.path.join(main_dir, 'translate.exe')
# running in a bundle
else:
    _2D_DNN_dir = os.path.join(main_dir, 'segment', '_2D_DNN')
    exec_run_translate = 'python ' + os.path.join(_2D_DNN_dir, 'translate.py')


# running live

class ExecuteTraining(MiscellaneousSegment):

    def __init__(self, obj_args, args):  # wxGlade: ImportImagesSegments.<event_handler>
        #
        # Dialog to specify directory
        #

        params = self.ObtainParams(obj_args, args)

        aug = params['Augmentation']
        if   aug == "fliplr, flipud, transpose":
            augmentation = '--fliplr --flipud --transpose'
        elif aug == "fliplr, flipud":
            augmentation = '--fliplr --flipud --no_transpose'
        elif aug == "fliplr":
            augmentation = '--fliplr --no_flipud --no_transpose'
        elif aug == "flipud":
            augmentation = '--no_fliplr --flipud --no_transpose'
        elif aug == "None":
            augmentation = '--no_fliplr --no_flipud --no_transpose'
        else :
            print("Internal error at Augumentation of PartDialogTrainingExecutor.")
            self._Cancel()
            return
        #
        print('Images and segmentation were merged.')
        #

        comm = exec_run_translate +' ' \
                + ' --mode train ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
                + ' --input_dir_B ' + params['Segmentation Folder'] + ' ' \
                + ' --output_dir ' + params['Checkpoint Folder'] + ' ' \
                + ' --which_direction AtoB ' +  ' ' \
                + ' --X_loss ' + params['X Loss Function'] + ' ' \
                + ' --Y_loss ' + params['Y Loss Function'] + ' ' \
                + ' --model ' + params['Model'] + ' ' \
                + ' --generator ' + params['Generator'] + ' ' \
                + ' ' + augmentation + ' ' \
                + ' --max_epochs ' + params['Maximal Epochs'] + ' ' \
                + ' --display_freq ' +  params['Display Frequency'] + ' ' \
                + ' --u_depth ' + params['U depth'] + ' ' \
                + ' --n_res_blocks ' + params['N res blocks'] + ' ' \
                + ' --n_highway_units ' + params['N highway units'] + ' ' \
                + ' --n_dense_blocks ' + params['N dense blocks'] + ' ' \
                + ' --n_dense_layers ' + params['N dense layers'] + ' '


        print(comm)
        print('Start training.')
        try:
            s.Popen(comm.split())
        except s.CalledProcessError as e:
            print("Error ocurrs in Traslate.py.")
            return

        return


