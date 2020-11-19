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

        modelpath =  u_info.tensorflow_model_path
        self.paramfile =  os.path.join( u_info.parameters_path, "Inference_2D.pickle")

        self.title = '2D Inference'

        self.tips = [
                        'Path to folder containing images',
                        'Path to folder for storing segmentation',
                        'Directory with checkpoint for training data'
                        ]


        self.args = [
                        ['Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Output Segmentation Folder (Empty)', 'SelectEmptyFolder', 'OpenEmptyFolder'],
                        ['Model Folder',  'SelectModelFolder', 'OpenModelFolder']
                        ]



