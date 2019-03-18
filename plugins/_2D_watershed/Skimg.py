###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir


from scipy import ndimage as ndi
from skimage.morphology import watershed
from skimage.feature    import peak_local_max

class Skimg():

    def Filter(self, input_image, params):

        binary_image = np.logical_not(input_image > params['Binarization threshold'])
        distance = ndi.distance_transform_edt(binary_image)
        local_maxi = peak_local_max(distance, min_distance=params['Min distance'], indices=False, footprint=np.ones((20, 20)))
        markers, n_markers = ndi.label(local_maxi)
        print('Number of markers: ', n_markers)
        labels = watershed(input_image, markers)

        return labels


    def __init__(self, u_info):

        datadir =  u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_inference")
        outpath =  os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters","Watershed2D_Skimg.pickle")

        self.filter_name = 'Skimg'

        self.tips = [
                        'Binarization threshold to obtain isolated peaks'
                        'Minimum number of pixels separating peaks'
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Binarization threshold', 'SpinBox', [1, 8, 256]],
                        ['Min distance', 'SpinBox', [1, 10, 256]],
                        ['Target Folder',    'LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder',   'LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '16'


