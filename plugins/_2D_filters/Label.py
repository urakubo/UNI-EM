###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

from skimage.measure import label

class Label():

    def Filter(self, input_image, params):

        processed_image = label(input_image, background=params['Background intensity'], \
                                        connectivity =params['Connectivity'])

        return processed_image


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_inference")
        outpath =  os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters", "Gaussian_2D.pickle")

        self.filter_name = 'Label'

        self.tips = [
                        'All pixels with this value are considered as background pixels',
                        'Maximum number of orthogonal hops to consider a pixel as a neighbor (1 or 2)',
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Background intensity', 'SpinBox', [0, 0, 255]],
                        ['Connectivity', 'SpinBox', [1, 2, 2]],
                        ['Target Folder', 'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder', 'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '16'

