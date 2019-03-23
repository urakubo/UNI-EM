###
###
###

import sys, os, time, errno

import numpy as np
import copy
from itertools import chain
import subprocess as s
import time
import cv2
import glob
import shutil

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

    def __init__(self, obj_args, args, parent):  # wxGlade: ImportImagesSegments.<event_handler>

        ##
        ## Check bitdepth of EM images and segmentation in the target directory.
        ## Translate.py only accepts unit24 (RGB color).
        ##

        #
        # Dialog to specify directory
        #

        params  = self.ObtainParams(obj_args, args)
        datadir = parent.u_info.data_path

        ##
        ## Check and change filetype of input images
        ##
        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        if len(input_paths) == 0:
            input_files = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        im = cv2.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('Target file to check color type : ', input_files[0])
        print('Image dimensions                : ', im.shape)
        print('Image filetype                  : ', im.dtype)
        if not (im.dtype == "uint8" and len(im.shape) == 3) :
            tmpdir = os.path.join(datadir, "tmp", "DNN_training_images")
            if os.path.exists(tmpdir) :
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            for input_file in input_files:
                im_col = cv2.imread(input_file)
                filename = os.path.basename(input_file)
                converted_input_file = os.path.join( tmpdir, filename )
                cv2.imwrite(converted_input_file, im_col)
            params['Image Folder'] = tmpdir
            print('Filetype of images was changed to RGB 8bit, and stored in ', tmpdir)

        ##
        ## Check and change filetype of input segmentation
        ##
        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        if len(input_paths) == 0:
            input_files = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        im = cv2.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('Target file to check color type : ', input_files[0])
        print('Segmentation image dimensions   : ', im.shape)
        print('Segmentation filetype           : ', im.dtype)
        if not (im.dtype == "uint8" and len(im.shape) == 3) :
            tmpdir = os.path.join(datadir, "tmp", "DNN_ground_truth")
            if os.path.exists(tmpdir) :
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            for input_file in input_files:
                im_col = cv2.imread(input_file)
                filename = os.path.basename(input_file)
                converted_input_file = os.path.join( tmpdir, filename )
                cv2.imwrite(converted_input_file, im_col)
            params['Segmentation Folder'] = tmpdir
            print('Filetype of segmentation was changed to RGB 8bit, and stored in', tmpdir)


        #
        # Dialog to specify directory
        #

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
        #   ' --model ' + params['Model'] + ' '
        #

        comm = exec_run_translate +' ' \
                + ' --mode train ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
                + ' --target_dir ' + params['Segmentation Folder'] + ' ' \
                + ' --output_dir ' + params['Checkpoint Folder'] + ' ' \
                + ' --loss ' + params['Loss Function'] + ' ' \
                + ' --network ' + params['Network'] + ' ' \
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

            ##
            ##
            ##
            s.Popen(comm.split())
        except s.CalledProcessError as e:
            print("Error ocurrs in Traslate.py.")
            return

        return


