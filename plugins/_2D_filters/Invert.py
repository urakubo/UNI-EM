###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

from PyQt5.QtCore import Qt
import cv2

class Invert():

    def Filter(self, input_image, params):
        processed_image = cv2.bitwise_not(input_image)
        return processed_image


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_inference")
        outpath =  os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters", "Invert_2D.pickle")

        self.filter_name = 'Invert'

        self.tips = [
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Target Folder', 'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder', 'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '8'

