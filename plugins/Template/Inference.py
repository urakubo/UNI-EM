##
##
##
import sys, os
import subprocess as s
import miscellaneous.Miscellaneous as m

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
# exec_template = ['python', os.path.join(main_dir, 'plugins', 'Template', 'run_example.py')]

class Inference():

    def _Run(self, parent, params, comm_title):
        ##
        tmp = [		'--test_image_folder'   			, params['Test image folder'] , \
					'--inferred_segmentation_folder'	, params['Inferred segmentation folder'] , \
					'--tensorflow_model_file' 			, params['Model Folder'] ]

        comm_run = self.u_info.exec_template[:]
        comm_run.extend( tmp )
        print('')
        print('  '.join(comm_run))
        print('')
        ##
        m.UnlockFolder(self.u_info, params['Inferred segmentation folder']) # Only for shared folder/file
        s.run(comm_run)
        m.LockFolder(self.u_info, params['Inferred segmentation folder'])
        print(comm_title, 'was finished.\n')
        ##
        return True

    def __init__(self, u_info):
        ##
        self.u_info = u_info
        self.paramfile = os.path.join(u_info.parameters_path, "Inference.pickle")

        self.title = 'Inference'

        self.tips = [
                        'Input: Path to folder containing target images',
                        'Output: Path to folder storing inferred images',
                        'Input: Tensorflow model Folder'
                    ]

        self.args = [
                        ['Test image folder', 'SelectImageFolder', 'OpenImageFolder'],
                        ['Inferred segmentation folder', 'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder',  'SelectModelFolder', 'OpenModelFolder']
                    ]

