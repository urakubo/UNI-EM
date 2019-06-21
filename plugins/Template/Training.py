##
##
import sys, os
import subprocess as s
from PyQt5.QtCore import Qt
import miscellaneous.Miscellaneous as m

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
#exec_template = 'python ' +  os.path.join(main_dir, 'plugins', 'run_example.py')


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
        comm_run = self.u_info.exec_template + ' ' \
                     + ' --training_image_folder '    + params['Training image folder'] + ' ' \
                     + ' --ground_truth_folder '      + params['Ground truth folder'] + ' ' \
                     + ' --tensorflow_model_folder ' + params['Tensorflow model folder']  + ' ' \
        ##
        print(comm_run)
        print('')
        s.run(comm_run.split())
        print(comm_title, 'was finished.\n')
        return True

    def Execute(self, parent, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)
        thread = threading.Thread(target=self._Run, args=( params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent.parent, 'Template',  comm_title + ' runs on a different process.')
        # parent.close()
        return

    def __init__(self, u_info):
        ##
        tensorflow_path = u_info.tensorflow_model_path
        
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
                        ['Tensorflow model folder', 'LineEdit', tensorflow_path, 'BrowseDir'],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['Sparse Z', 'CheckBox', False],
                        ['Mode', 'ComboBox', ['a','b','c']]
            ]

