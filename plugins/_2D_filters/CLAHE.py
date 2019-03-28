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


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "DNN_segmentation")
        outpath =  os.path.join(datadir, "DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters","Watershed2D_Skimg.pickle")

        self.filter_name = 'CLAHE'

        self.tips = [
                        'contrast limitation to avoid noise amplification.'
                        'Image is divided into "tiles" (small blocks), \\n and each of these blocks are histogram equalized.'
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Clip Limit', 'SpinBox', [1, 2, 256]],
                        ['Tile Size', 'SpinBox', [1, 8, 256]],
                        ['Target Folder',    'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder',   'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '16'


