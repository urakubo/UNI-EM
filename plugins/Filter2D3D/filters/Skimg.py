###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir


from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature    import peak_local_max

class Skimg():

    def Filter(self, input_image, params):

        binary_image = np.logical_not(input_image > params['Binarization threshold'])
        distance = ndi.distance_transform_edt(binary_image)
        local_maxi = peak_local_max(distance, labels=binary_image, min_distance=params['Min distance'])
        mask = np.zeros(distance.shape, dtype=bool)
        mask[tuple(local_maxi.T)] = True
        markers, n_markers = ndi.label(mask)
        print('Number of markers: ', n_markers)
        labels = watershed(-distance, markers, mask=binary_image)

        return labels


    def __init__(self):
        self.tips = [
                        'Binarization threshold to obtain isolated peaks',
                        'Minimum number of pixels separating peaks',
                        ]

        self.args = [
                        ['Binarization threshold', 'SpinBox', [1, 8, 256]],
                        ['Min distance', 'SpinBox', [1, 10, 256]],
            ]


