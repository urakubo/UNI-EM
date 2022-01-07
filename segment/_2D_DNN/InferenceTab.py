###
###
###
import sys, os, time, errno
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))
from _2D_DNN.InferenceExe import InferenceExe

class InferenceTab(InferenceExe):

    def __init__(self, u_info):

        self.paramfile =  os.path.join( u_info.parameters_path, "Inference_2D.pickle")

        self.title = '2D Inference'

        self.tips = [
                        'Path to folder containing images for inference',
                        'Tensorflow model folder',
                        'Path to folder to store inferred segmentation',
                        'Output Filetype',
                        'Unit size of images for inference. Large image will be splited into pieces of the unit-size images.'
                        ]


        self.args = [
                        ['Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder',  'SelectModelFolder', 'OpenModelFolder'],
                        ['Output Segmentation Folder (Empty)', 'SelectEmptyFolder', 'OpenEmptyFolder'],
                        ['Output Filetype',  'ComboBox', ['8-bit gray scale PNG', '8-bit gray scale TIFF (Uncompressed)', '8-bit gray scale TIFF (Compressed)', '24-bit RGB TIFF (Uncompressed)']],
                        ['Maximal unit image size',  'ComboBox', ["512", "1024", "2048"]]
                        ]



