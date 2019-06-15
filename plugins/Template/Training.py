###
###
###
import sys, os
import numpy as np
import subprocess as s
from PyQt5.QtCore import Qt
from MiscellaneousTemplate import MiscellaneousTemplate
import miscellaneous.Miscellaneous as m

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")

##
exec_dir = os.path.join(main_dir, 'plugins','Template')
exec_template = 'python ' +  os.path.join(exec_dir, 'run_example.py')
##

class Training(MiscellaneousTemplate):
    def _Run(self, params, comm_title):
        ##
        if params['Sparse Z'] != Qt.Unchecked:
            print('Sparse Z           : checked')
        else:
            print('Sparse Z           : unchecked')
        print('Checkpoint Interval: ', params['Checkpoint Interval'])
        print('Mode               : ', params['Mode'])
        ##
        comm_run = exec_template + ' ' \
                     + ' --training_image_folder '    + params['Training image folder'] + ' ' \
                     + ' --ground_truth_folder '      + params['Ground truth folder'] + ' ' \
                     + ' --tensorflow_model_folder ' + params['Tensorflow model folder']  + ' ' \
        ##
        print(comm_run)
        print('')
        s.run(comm_run.split())
        print(comm_title, 'was finished.\n')
        return True

    def __init__(self, u_info):
        ##
        tensorflow_path = u_info.tensorflow_model_path
        self.paramfile = os.path.join(u_info.parameters_path, "Training.pickle")

        self.name = 'Training'

        self.tips = [
                        'Input : Training image folder',
                        'Input : Ground truth folder',
                        'Input/Output: Tensorlflow Model Folder',
                        'Checkpoint Interval',
                        'Sparse Z',
                        'Mode'
                        ]

        self.args = [
                        ['Training image folder', 'SelectOpenImage', 'OpenImage'],
                        ['Ground truth folder', 'SelectOpenImage', 'OpenImage'],
                        ['Tensorflow model folder', 'LineEdit', tensorflow_path, 'BrowseDir'],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['Sparse Z', 'CheckBox', False],
                        ['Mode', 'ComboBox', ['a','b','c']]
            ]

