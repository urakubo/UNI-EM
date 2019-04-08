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


    def __init__(self):
        self.tips = []

        self.args = []

        self.output_bitdepth = '8'

