###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir


from scipy import ndimage as ndi
from skimage.morphology import watershed
from skimage.feature    import peak_local_max

class Skimg3D():

    def Filter(self, input_image, params):

        binary_image = np.logical_not(input_image > params['Binarization threshold'])
        distance = ndi.distance_transform_edt(binary_image)
        local_maxi = peak_local_max(distance, min_distance=params['Min distance'], indices=False )
        markers, n_markers = ndi.label(local_maxi)
        print('Number of markers: ', n_markers)
        labels = watershed(input_image, markers)

        return labels


    def __init__(self):
        self.tips = [
                        'Binarization threshold to obtain isolated peaks',
                        'Minimum number of pixels separating peaks',
                        ]

        self.args = [
                        ['Binarization threshold', 'SpinBox', [1, 20, 256]],
                        ['Min distance', 'SpinBox', [1, 18, 256]],
            ]


