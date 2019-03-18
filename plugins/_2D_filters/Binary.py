###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

from PyQt5.QtCore import Qt
import cv2

class Binary():

    def Filter(self, input_image, params):
        if params['Invert'] == Qt.Checked:
            ret,processed_image = cv2.threshold(input_image, params['Threshold'], params['Max value'], cv2.THRESH_BINARY_INV)
        else :
            ret,processed_image = cv2.threshold(input_image, params['Threshold'], params['Max value'], cv2.THRESH_BINARY)

        return processed_image


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_inference")
        outpath =  os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters", "Binary_2D.pickle")

        self.filter_name = 'Binary'

        self.tips = [
                        'Threshold of separation',
                        'Maximum value',
                        'Inverse step',
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Threshold', 'SpinBox', [0, 127, 255]],
                        ['Max value', 'SpinBox', [0, 255, 255]],
                        ['Invert', 'CheckBox', False ],
                        ['Target Folder', 'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder', 'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '8'

