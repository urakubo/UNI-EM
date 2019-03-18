###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

from skimage.feature import canny

class Canny():

    def Filter(self, input_image, params):

        processed_image = canny(input_image, sigma=params['Standard deviation'])

        return processed_image


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_inference")
        outpath =  os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters", "Canny_2D.pickle")

        self.filter_name = 'Edge (Canny)'

        self.tips = [
                        'Standard deviation of the Gaussian filter',
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Standard deviation', 'SpinBox', [1, 4, 255]],
                        ['Target Folder', 'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder', 'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '8'

