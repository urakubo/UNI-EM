##
##
import sys, os
import subprocess as s
from PyQt5.QtCore import Qt
import miscellaneous.Miscellaneous as m

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
# exec_template = ['python', os.path.join(main_dir, 'plugins', 'Template', 'run_example.py')]


class Training():
    def _Run(self, parent, params, comm_title):
        ##
        if params['Sparse Z'] != Qt.Unchecked:
            print('Sparse Z           : checked')
        else:
            print('Sparse Z           : unchecked')
        print('Checkpoint Interval: ', params['Checkpoint Interval'])
        print('Mode               : ', params['Mode'])
        ##
        tmp = [	'--training_image_folder'   , params['Training image folder']	, \
                    '--ground_truth_folder'     , params['Ground truth folder']	, \
                    '--tensorflow_model_file'   , params['Model Folder (Empty/Model)'] ]
        comm_run = self.u_info.exec_template[:]
        comm_run.extend( tmp )
        ##
        print('')
        print('  '.join(comm_run))
        print('')
        s.run(comm_run)
        print(comm_title, 'was finished.\n')
        return True


    def __init__(self, u_info):
        ##
        self.u_info = u_info
        
        self.paramfile = os.path.join(u_info.parameters_path, "Training.pickle")

        self.title = 'Training'

        self.tips = [
                        'Input : Training image folder',
                        'Input : Ground truth folder',
                        'Input/Output: Tensorlflow Model Folder',
                        'Checkpoint Interval',
                        'Sparse Z',
                        'Mode'
                        ]

        self.args = [
                        ['Training image folder', 'SelectImageFolder', 'OpenImageFolder'],
                        ['Ground truth folder', 'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder (Empty/Model)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder'],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['Sparse Z', 'CheckBox', False],
                        ['Mode', 'ComboBox', ['a','b','c']]
            ]

