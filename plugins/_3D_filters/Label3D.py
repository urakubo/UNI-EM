###
###
###
import sys, os, time, errno
import numpy as np
from os import path, pardir


from scipy import ndimage as ndi

from skimage.measure import label

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))


class Label3D():


    def Filter(self, input_image, params):

        labels = label(input_image, background=params['Background intensity'], \
                                        connectivity =params['Connectivity'])

        return labels


    def __init__(self, u_info):

        datadir = u_info.data_path
        imgpath = os.path.join(datadir, "_2DNN_inference")
        outpath = os.path.join(datadir, "_2DNN_segmentation")
        self.paramfile = os.path.join(datadir, "parameters","Filter3D_Label.pickle")

        self.filter_name = 'Label'

        self.tips = [
                        'All pixels with this value are considered as background pixels',
                        'Maximum number of orthogonal hops to consider a pixel as a neighbor (1 - 3)',
                        'Path to folder containing images',
                        'Path to folder for storing results'
                        ]


        self.args = [
                        ['Background intensity', 'SpinBox', [0, 0, 255]],
                        ['Connectivity', 'SpinBox', [1, 3, 3]],
                        ['Target Folder','LineEdit', imgpath, 'Browsedir'],
                        ['Output Folder','LineEdit', outpath, 'Browsedir']
            ]

        self.output_bitdepth = '16'

