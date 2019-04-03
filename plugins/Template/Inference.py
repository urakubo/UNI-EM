###
###
###
import sys, os
import numpy as np
import subprocess as s
from MiscellaneousTemplate import MiscellaneousTemplate

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")

#######
exec_dir = os.path.join(main_dir, 'plugins','Template')
exec_template = 'python ' +  os.path.join(exec_dir, 'run_example.py')

class Inference(MiscellaneousTemplate):

    def _Run(self, params, comm_title):
        ##
        comm_run = exec_template + ' ' \
                    + ' --test_image_folder '   + params['Test image folder'] + ' ' \
                    + ' --inferred_segmentation_folder '     + params['Inferred segmentation folder'] + ' ' \
                    + ' --tensorflow_model_file ' + params['Tensorflow model file']  + ' ' \
        ##
        print(comm_run)
        print('')
        s.run(comm_run.split())
        print(comm_title, 'was finished.\n')
        return True

    def __init__(self, u_info):
        ##
        datadir = u_info.data_path
        test_image_path      = os.path.join(datadir, "DNN_test_images")
        inferred_seg_path    = os.path.join(datadir, "DNN_segmentation")
        tensorflow_file      = os.path.join(datadir, "DNN_model_tensorflow","model.tf")
        self.paramfile = os.path.join(datadir, "parameters", "Inference.pickle")

        self.name = 'Inference'

        self.tips = [
                        'Input: Path to folder containing target images',
                        'Output: Path to folder storing inferred images',
                        'Input: Tensorflow model Files'
                    ]

        self.args = [
                        ['Test image folder'   , 'LineEdit', test_image_path  , 'BrowseDirImg'],
                        ['Inferred segmentation folder'     , 'LineEdit', inferred_seg_path    , 'BrowseDir'],
                        ['Tensorflow model file' , 'LineEdit', tensorflow_file , 'BrowseFile'],
                    ]

