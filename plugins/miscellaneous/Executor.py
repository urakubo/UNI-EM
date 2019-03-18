###
###
###

import sys, os, time, errno

from PIL import Image
import numpy as np
import copy
from itertools import chain
import subprocess as s
import time
import glob     # Wild card
import cv2
import threading

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "filesystem"))

# from Watershed import Watershed
import Miscellaneous as m
from MiscellaneousPlugins  import MiscellaneousPlugins

class Executor(MiscellaneousPlugins):

    ##
    def _Run(self,  filter, filter_name, params, filestack, output_path, output_bitdepth):
    ##
        print('Output Folder: ', output_path)
        for zi, filename in enumerate(filestack):
            #
            print('No:', zi)
            #
            input_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            #
            output_image = filter(input_image, params)

            # Output segmentation
            output_name = os.path.basename(filename)
            savename = os.path.join(output_path, output_name)
            root, ext = os.path.splitext(savename)
            if ext == ".tif" or ext == ".tiff" or ext == ".TIF" or ext == ".TIFF":
                if output_bitdepth == '16':
                    m.save_tif16(output_image, savename)
                elif output_bitdepth == '8':
                    m.save_tif8(output_image, savename)
            elif ext == ".png" or ext == ".PNG":
                if output_bitdepth == '16':
                    m.save_png16(output_image, savename)
                elif output_bitdepth == '8':
                    m.save_png8(output_image, savename)
        print(filter_name, 'was executed!')


    ##
    def __init__(self, parent, filter, filter_name, obj_args, args, output_bitdepth ):  # wxGlade: ImportImagesSegments.<event_handler>
    ##

    ## Obtain parameters

        params = self.ObtainParams(obj_args, args)
        #
        input_path  = params['Target Folder']
        output_path = params['Output Folder']
        print( 'Target Folder: ' , input_path  )

        #
        search1  = os.path.join(input_path,'*.png')
        search2  = os.path.join(input_path,'*.tif')
        search3  = os.path.join(input_path, '*.tiff')
        filestack = sorted(glob.glob(search1))
        filestack.extend( sorted(glob.glob(search2)) )
        filestack.extend(sorted(glob.glob(search3)))
        if filestack == [] :
            print('No PNG/TIFF images.')
            QMessageBox.about(parent, filter_name, filter_name + ': No PNG/TIFF images.')
            # self.close()
            return

    ## Run watershed

        thread = threading.Thread(target=self._Run, args=( filter, filter_name, params, filestack, output_path, output_bitdepth) )
        thread.daemon = True
        thread.start()

        QMessageBox.about(parent, filter_name,  filter_name + ' runs on a different process.')

        # parent.close()
        return

