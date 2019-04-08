###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir

from PyQt5.QtCore import Qt
import cv2

class CLAHE():

    def Filter(self, input_image, params):

        clahe = cv2.createCLAHE(clipLimit=params['Clip Limit'], tileGridSize=(params['Tile Size'], params['Tile Size']))
        processed_image = clahe.apply(input_image)

        return processed_image


    def __init__(self):
        self.tips = [
                        'contrast limitation to avoid noise amplification.'
                        'Image is divided into "tiles" (small blocks), \\n and each of these blocks are histogram equalized.'
                        ]

        self.args = [
                        ['Clip Limit', 'SpinBox', [1, 2, 256]],
                        ['Tile Size', 'SpinBox', [1, 8, 256]],
            ]

        self.output_bitdepth = '16'


