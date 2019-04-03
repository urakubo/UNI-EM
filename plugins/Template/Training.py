###
###
###
import sys, os
import numpy as np
import subprocess as s
from PyQt5.QtCore import Qt
from MiscellaneousTemplate import MiscellaneousTemplate

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")

###
exec_dir = os.path.join(main_dir, 'plugins','Template')
exec_train = 'python ' +  os.path.join(exec_dir, 'run_example.py')
###

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
        comm_train = exec_train + ' ' \
                     + ' --training_image_folder '    + params['Training image folder'] + ' ' \
                     + ' --ground_truth_folder '      + params['Ground truth folder'] + ' ' \
                     + ' --tensorflow_model_folder ' + params['Tensorflow model folder']  + ' ' \
        ##
        print(comm_train)
        print('')
        s.run(comm_train.split())
        print(comm_title, 'was finished.\n')
        return True

    def __init__(self, u_info):
        ##
        datadir = u_info.data_path
        training_image_path  = os.path.join(datadir, "DNN_training_images")
        ground_truth_path    = os.path.join(datadir, "DNN_ground_truth")
        tensorflow_file_path = os.path.join(datadir, "DNN_model_tensorflow")
        self.paramfile = os.path.join(datadir, "parameters", "Training.pickle")

        self.name = 'Training'

        self.tips = [
                        'Checkpoint Interval',
                        'Sparse Z',
                        'Mode',
                        'Input : Training image folder',
                        'Input : Ground truth folder',
                        'Input/Output: Tensorlflow Model Folder'
                        ]

        self.args = [
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['Sparse Z', 'CheckBox', False],
                        ['Mode', 'ComboBox', ['a','b','c']],
                        ['Training image folder'   , 'LineEdit', training_image_path   , 'BrowseDirImg'],
                        ['Ground truth folder'     , 'LineEdit', ground_truth_path     , 'BrowseDirImg'],
                        ['Tensorflow model folder' , 'LineEdit', tensorflow_file_path  , 'BrowseDir'],
            ]
        ##
