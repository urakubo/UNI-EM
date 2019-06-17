###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

import cv2

class Gaussian():

    def Filter(self, input_image, params):

        # print(input_image.dtype)
        processed_image = cv2.GaussianBlur(input_image, (0, 0), params['Standard deviation'])

        return processed_image


    def __init__(self):
        self.tips = [
                        'Minimum number of pixels separating peaks',
                        ]


        self.args = [
                        ['Standard deviation', 'SpinBox', [1, 5, 256]],
            ]

        self.output_bitdepth = '8'

