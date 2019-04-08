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
        processed_image = processed_image.astype('uint16')

        return processed_image


    def __init__(self):
        self.tips = [
                        'All pixels with this value are considered as background pixels',
                        'Maximum number of orthogonal hops to consider a pixel as a neighbor (1 or 2)',
                        ]

        self.args = [
                        ['Background intensity', 'SpinBox', [0, 0, 255]],
                        ['Connectivity', 'SpinBox', [1, 2, 2]],
            ]


