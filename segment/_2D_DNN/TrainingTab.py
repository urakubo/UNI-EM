###
###
###
import sys, os, time, errno


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))

from _2D_DNN.TrainingExe import TrainingExe
from miscellaneous.SyncListQComboBoxManager import *

class TrainingTab(TrainingExe):
    def __init__(self, u_info):

        modelpath =  u_info.tensorflow_model_path
        self.paramfile =  os.path.join( u_info.parameters_path, "Training_2D.pickle")

        self.title = '2D Training'

        self.tips = [
                        'Path to folder containing images',
                        'Path to folder containing segmentation',
                        'Directory with checkpoint to resume training from or use for testing',
                        'Network topology',
                        'Depth of U-net (maximum 8)',
                        'Number of residual blocks in res net',
                        'Number of highway units in highway net',
                        'Number of dense blocks in dense net',
                        'Number of dense connected layers in each block of the dense net',
                        'Number of images in batch',
                        'Loss Function',
                        'Number of training epochs',
                        'Write current training images every display frequency steps',
                        'Dimensions for Augmentation'
                        ]

        self.args = [
                        ['Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Segmentation Folder',   'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder',      'LineEdit', modelpath, 'BrowseDir'],
                        ['Network', 'Tab', ['unet', 'resnet', 'highwaynet', 'densenet'], [0,1,2,3,3] ],
                        ['U depth','SpinBox',[1,8,20]],
                        ['N res blocks','SpinBox',[1,9,255]],
                        ['N highway units','SpinBox',[1,9,255]],
                        ['N dense blocks','SpinBox',[1,5,255]],
                        ['N dense layers','SpinBox',[1,5,255]],
                        ['Batch Size', 'SpinBox', [1, 1, 65535]],
                        ['Loss Function', 'ComboBox', ["softmax", "hinge", "square", "approx", "dice", "logistic"]],
                        ['Maximal Epochs', 'SpinBox', [1, 2000, 65535]],
                        ['Display Frequency', 'SpinBox', [0, 200, 65535]],
                        ['Augmentation',  'ComboBox', ["fliplr, flipud, transpose", "fliplr, flipud", "fliplr", "flipud", "None"]]
                        ]


