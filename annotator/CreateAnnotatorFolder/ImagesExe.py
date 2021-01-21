###
###
###

import sys, os, time, errno
from os import path, pardir
import glob
import numpy as np
import json
import sqlite3
import h5py
import cv2


main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
#sys.path.append(path.join(main_dir, "system"))
import miscellaneous.Miscellaneous as m


class ImagesExe():

    def _Run(self, parent, params, comm_title):

        print('Annotator folder is generated for', comm_title)
        img_files = glob.glob(os.path.join(params['Segmentation image Folder'], "*.png"))# PNG
        img_files.extend( glob.glob(os.path.join(params['Segmentation image Folder'], "*.PNG")) )# PNG
        img_files.extend( glob.glob(os.path.join(params['Segmentation image Folder'], "*.tif")) )# TIFF
        img_files.extend( glob.glob(os.path.join(params['Segmentation image Folder'], "*.tiff")) )# TIFF
        img_files = sorted(img_files)
        if len(img_files) == 0:
            print('No tif/png file.')
            return

        comm = parent.u_info.exec_translate[:]
        comm.extend( tmp )

        parent.parent.ExecuteCloseFileFolder(params['Empty Folder for Annotator'])
        parent.parent.OpenFolder(params['Empty Folder for Annotator'])
        print('')
        print('Annotator folder created.')
        print('')
        return True



