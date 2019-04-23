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
import shutil
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

class ExecuteInference(MiscellaneousSegment):

    def __init__(self, obj_args, args, parent):  # wxGlade: ImportImagesSegments.<event_handler>
        ##
        ## Dialog to specify directory
        ##
        params = self.ObtainParams(obj_args, args)
        datadir = parent.u_info.data_path


        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        if len(input_files) == 0:
            input_files = glob.glob(os.path.join(params['Image Folder'], "*.png"))
            if len(input_files) == 0:
                print('No images in the Image Folder.')
                return

        im = cv2.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('Target file to check color type : ', input_files[0])
        print('Image dimensions                : ', im.shape)
        print('Image filetype                  : ', im.dtype)
        image_width  = im.shape[0]
        image_height = im.shape[1]

        if not (im.dtype == "uint8" and len(im.shape) == 3) :
            tmpdir = os.path.join(datadir, "tmp", "DNN_test_images")
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


        comm = parent.u_info.exec_translate +' ' \
                + ' --mode predict ' \
                + ' --save_freq 0 ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
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

