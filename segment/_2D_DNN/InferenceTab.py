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
                        'Path to folder containing images',
                        'Path to folder to store segmentation',
                        'Tensorflow model folder',
                        'Large image will be splited into pieces of the unit images'
                        ]


        self.args = [
                        ['Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Output Segmentation Folder (Empty)', 'SelectEmptyFolder', 'OpenEmptyFolder'],
                        ['Model Folder',  'SelectModelFolder', 'OpenModelFolder'],
                        ['Maximal unit image size',  'ComboBox', ["512", "1024", "2048"]]
                        ]



