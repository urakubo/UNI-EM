###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

import cv2

class Gaussian():

    def Filter(self, input_image, params):

        processed_image = cv2.GaussianBlur(input_image, (0, 0), params['Standard deviation'])

        return processed_image


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_inference")
        outpath =  os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters", "Gaussian_2D.pickle")

        self.filter_name = 'Gaussian Blur'

        self.tips = [
                        'Minimum number of pixels separating peaks'
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Standard deviation', 'SpinBox', [1, 5, 256]],
                        ['Target Folder', 'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder', 'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '8'

