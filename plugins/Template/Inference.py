###
###
###
import sys, os
import numpy as np
import subprocess as s
from miscellaneous.MiscellaneousTemplate import MiscellaneousTemplate
import miscellaneous.Miscellaneous as m

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
                    + ' --tensorflow_model_file ' + params['Tensorflow model file']  + ' '
        print(comm_run)
        print('')
        ##
        m.UnlockFolder(self.u_info, params['Inferred segmentation folder']) # Only for shared folder/file
        s.run(comm_run.split())
        m.LockFolder(self.u_info, params['Inferred segmentation folder'])
        print(comm_title, 'was finished.\n')
        ##
        return True

    def __init__(self, u_info):
        ##
        self.u_info = u_info
        tensorflow_file = os.path.join(u_info.tensorflow_model_path,"model.tf")
        self.paramfile = os.path.join(u_info.parameters_path, "Inference.pickle")

        self.name = 'Inference'

        self.tips = [
                        'Input: Path to folder containing target images',
                        'Output: Path to folder storing inferred images',
                        'Input: Tensorflow model Files'
                    ]

        self.args = [
                        ['Test image folder', 'SelectOpenImage', 'OpenImage'],
                        ['Inferred segmentation folder', 'SelectOpenImage', 'OpenImage'],
                        ['Tensorflow model file' , 'LineEdit', tensorflow_file , 'BrowseFile'],
                    ]

