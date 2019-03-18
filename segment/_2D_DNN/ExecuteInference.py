###
###
###

import sys, os, time, errno

import numpy as np
import copy
from itertools import chain
import subprocess as s
import time

import glob     # Wild card
import cv2

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "filesystem"))

from MiscellaneousSegment import MiscellaneousSegment

if getattr(sys, 'frozen', False):
    exec_run_translate = os.path.join(main_dir, 'translate.exe')
# running in a bundle
else:
    _2D_DNN_dir = os.path.join(main_dir, 'segment', '_2D_DNN')
    exec_run_translate = 'python ' + os.path.join(_2D_DNN_dir, 'translate.py')


class ExecuteInference(MiscellaneousSegment):

    def __init__(self, obj_args, args):  # wxGlade: ImportImagesSegments.<event_handler>
        ##
        ## Dialog to specify directory
        ##
        params = self.ObtainParams(obj_args, args)

        filestack = self.ObtainImageFiles(params['Image Folder'])
        if len(filestack) == 0:
            print('No images in the Image Folder.')
            return

        input_image = cv2.imread(filestack[0], cv2.IMREAD_GRAYSCALE)
        image_width, image_height = input_image.shape

        comm = exec_run_translate +' ' \
                + ' --mode test ' \
                + ' --model pix2pix ' \
                + ' --save_freq 0 ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
                + ' --input_dir_B ' + params['Image Folder'] + ' ' \
                + ' --output_dir ' + params['Output Segmentation Folder'] + ' ' \
                + ' --checkpoint ' + params['Checkpoint Folder'] + ' ' \
                + ' --image_height ' + str(image_height) + ' ' \
                + ' --image_width ' + str(image_width)
        # - -image_height 1024
        # - -image_width 1024


        try:
            print(comm)
            print('Start inference.')
            s.Popen(comm.split())
        except subprocess.CalledProcessError as e:
            print("Inference was not executed.")
            return
        return

