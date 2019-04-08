###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

# from skimage.feature import canny
import cv2

class Canny():

    def Filter(self, input_image, params):

        # processed_image = canny(input_image, sigma=params['Standard deviation'])
        processed_image = cv2.Canny(input_image, params['Lower threshold'], params['Upper threshold'])
        processed_image = processed_image.astype('uint8')
        return processed_image


    def __init__(self):
        self.tips = [
                        'If an edge is above this value, it is considered as "sure-edge".',
                        'If an edge is below this value, it is not considered as an edge.'
                        ]

        self.args = [
                        ['Upper threshold', 'SpinBox', [1, 200, 255]],
                        ['Lower threshold', 'SpinBox', [1, 100, 255]]
            ]

        self.output_bitdepth = '8'

