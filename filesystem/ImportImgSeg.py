#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import cv2
import png
import glob     # Wild card
import shutil
# import argparse # Argument
import numpy as np

##
from os import path, pardir
current_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
sys.path.append(path.join(parent_dir, "Filesystem"))
from Params import Params
from np2imgo import Imgo
from np2sego import Sego
from np2sego_dummy import Sego_dummy
##

##
class ImportImgSeg():

    ###
    ###
    def __init__(self, u_info):
        self.u_info = u_info
    ###
    ###

    def main( self, outfile, stack ):
        # Size input files
        sample_slice = cv2.imread(stack[0], cv2.IMREAD_UNCHANGED)
        sliceShape   = sample_slice.shape[0:2]
        sliceGrayCol = sample_slice.ndim # 2. gray; 3, RGB
        sliceDepth   = sample_slice.dtype
        shape = (len(stack),) + sliceShape

        # Add each png file as a slice
        for zi, file in enumerate(stack):
            if sliceGrayCol == 2 :
                written = cv2.imread(file, cv2.IMREAD_UNCHANGED) # .astype(dtype)
            else:
                # Buggy ...
                # volume  = cv2.imread(file, cv2.IMREAD_UNCHANGED)
                # written =  (volume[:,:,0] + volume[:,:,1] + volume[:,:,2]) / 3

                written = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
                # written = cv2.imread(file, -1)
            # Write as image or segmentation
            outfile.run(written, zi)
        # Write metadata to ouput file
        outfile.save(shape)

    ###
    def images( self, input_images_path ):
        # read all pngs in pngs folder
        search1 = os.path.join(input_images_path,'*.png')
        search2 = os.path.join(input_images_path,'*.tif')
        search3 = os.path.join(input_images_path, '*.tiff')
        stack   = sorted(glob.glob(search1))
        stack.extend( sorted(glob.glob(search2)) )
        stack.extend( sorted(glob.glob(search3)) )
        if stack == [] :
            print('No PNG/TIFF images.')
            return False
        outfile = Imgo( self.u_info )
        self.main( outfile, stack )
        return True

    def ids( self, input_ids_path ):
        # read all pngs in pngs folder
        search1 = os.path.join(input_ids_path,'*.png')
        search2 = os.path.join(input_ids_path,'*.tif')
        search3 = os.path.join(input_ids_path,'*.tiff')
        stack   = sorted(glob.glob(search1))
        stack.extend( sorted(glob.glob(search2)) )
        stack.extend( sorted(glob.glob(search3)) )
        if stack == [] :
            print('No PNG/TIFF segments.')
            return False
        outfile = Sego( self.u_info )
        self.main( outfile, stack )
        return True


    def ids_dummy( self, input_image_path ):
        # read all pngs in pngs folder
        search1 = os.path.join(input_image_path,'*.png')
        search2 = os.path.join(input_image_path,'*.tif')
        search3 = os.path.join(input_image_path,'*.tiff')
        stack   = sorted(glob.glob(search1))
        stack.extend( sorted(glob.glob(search2)) )
        stack.extend( sorted(glob.glob(search3)) )
        if stack == [] :
            print('No PNG/TIFF segments.')
            return False
        outfile = Sego_dummy( self.u_info )
        self.main( outfile, stack )
        return True

