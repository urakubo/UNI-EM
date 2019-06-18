###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir
# main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
# sys.path.append(main_dir)
# sys.path.append(os.path.join(main_dir, "filesystem"))

from Watershed import Watershed

class Mzur():

    def Filter(self, input_image, params):

        # in_shape = input_image.shape
        # original_image = np.zeros(in_shape, dtype=input_image.dtype)
        # original_image[:in_shape[0], :in_shape[1]] = input_image
        w = Watershed()
        # labels = w.apply(original_image)

        labels = w.apply(input_image)
        return labels


    def __init__(self):
        self.tips = []

        self.args = []

        self.output_bitdepth = '16'



