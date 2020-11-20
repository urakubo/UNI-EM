###
###
###
import sys, os, errno
import glob
import numpy as np
import subprocess as s
import fnmatch
import cv2
import h5py
# import threading

import contextlib

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
import miscellaneous.Miscellaneous as m
icon_dir = path.join(main_dir, "icons")
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))


##
##
##

class FFNInference():

    def write_text(self, f, key, value, t):
        if isinstance(value, str):
            f.write(' {0}{1}: "{2}" \n'.format(t, key, value ) )
        else:
            f.write(' {0}{1}: {2} \n'.format(t, key, value))

    def write_call(self, f, request, t):
        for key, value in request.items():
            if isinstance(request[key], dict):
                f.write('{} {{\n'.format(key))
                tid = t + "  "
                self.write_call(f, request[key], tid)
                f.write('}\n')
            else:
                self.write_text(f, key, value, t)

    def _Run(self, parent, params, comm_title):

        m.UnlockFolder(parent.u_info,  params['FFNs Folder'])

        ##
        ## Remove preovious results.
        ##
        removal_file1 = os.path.join( params['FFNs Folder'] ,'0','0','seg-0_0_0.npz' )
        removal_file2 = os.path.join( params['FFNs Folder'], '0','0','seg-0_0_0.prob')

        if os.path.isfile(removal_file1) or os.path.isfile(removal_file2) :
            Reply = QMessageBox.question(parent, 'FFN', 'seg-0_0_0 files were found in the FFNs Folder. Remove them?',  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if Reply == QMessageBox.Yes:
                with contextlib.suppress(FileNotFoundError):
                    os.remove(removal_file1)
                with contextlib.suppress(FileNotFoundError):
                    os.remove(removal_file2)
                print('seg-0_0_0 files were removed.')
            else:
                print('FFN inference was canceled.')
                m.LockFolder(parent.u_info,  params['FFNs Folder'])
                return

        ##
        ## h5 file (target image file) generation.
        ##
        target_image_file_h5 = os.path.join(params['FFNs Folder'], "grayscale_inf.h5")

        try:
            target_image_files = m.ObtainImageFiles(params['Target Image Folder'])
            images = [m.imread(i, cv2.IMREAD_GRAYSCALE) for i in target_image_files]
            images = np.array(images)
            image_z    = images.shape[0]
            image_y    = images.shape[1]
            image_x    = images.shape[2]
            image_mean = np.mean(images).astype(np.int16)
            image_std  = np.std(images).astype(np.int16)

            print('')
            print('x: {}, y: {}, z: {}'.format(image_x, image_y, image_z))
            with h5py.File( target_image_file_h5 , 'w') as f:
                f.create_dataset('raw', data=images, compression='gzip')
            print('"grayscale_inf.h5" file (target inference image) was generated.')
            print('')
        except:
            print('')
            print("Error: Target Image h5 was not generated.")
            m.LockFolder(parent.u_info,  params['FFNs Folder'])
            return False

        ##
        ## Tensorflow model extracted
        ##

        max_id_model = self.SelectMaxModel(params['Model Folder'] )
        print( 'Tensorflow model : ', max_id_model )
        
        if max_id_model == False:
            print('Cannot find tensorflow model.')
            return False

        ##
        ## Inference configration file generation
        ##
        request = {}
        request['image'] = {"hdf5": "{}@raw".format(target_image_file_h5).replace('\\', '/') }
        request['image_mean'] = image_mean
        request['image_stddev'] = image_std
        request['checkpoint_interval'] = int(params['Checkpoint Interval'])
        request['seed_policy'] = "PolicyPeaks"
        request['model_checkpoint_path'] = max_id_model.replace('\\', '/')
        request['model_name'] = "convstack_3d.ConvStack3DFFNModel"

        if params['Sparse Z'] != Qt.Unchecked:
            request['model_args'] = "{\\\"depth\\\": 9, \\\"fov_size\\\": [33, 33, 17], \\\"deltas\\\": [8, 8, 4]}"
            #request['model_args'] = ' {"depth":9,"fov_size":[33,33,17],"deltas":[8,8,4]} '
        else :
            request['model_args'] = "{\\\"depth\\\": 12, \\\"fov_size\\\": [33, 33, 33], \\\"deltas\\\": [8, 8, 8]}"
            #request['model_args'] = ' {"depth":12,"fov_size":[33,33,33],"deltas":[8,8,8]} '

        request['segmentation_output_dir'] = params['FFNs Folder'].replace('\\', '/')
        inference_options = {}
        inference_options['init_activation'] = 0.95
        inference_options['pad_value'] = 0.05
        inference_options['move_threshold'] = 0.9
        inference_options['min_boundary_dist'] = {"x": 1, "y": 1, "z": 1}
        inference_options['segment_threshold'] = 0.6
        inference_options['min_segment_size'] = 1000
        request['inference_options'] = inference_options


        config_file = os.path.join(params['FFNs Folder'], "inference_params.pbtxt")
        with open(config_file, "w", encoding='utf-8') as f:
            self.write_call(f, request, "")

        print('')
        print('Configuration file was saved at :')
        print(config_file)
        print('')
        ##
        ## Inference start (I gave up the use of run_inference because of the augment parsing problem)
        ##
        m.mkdir_safe(os.path.join( params['FFNs Folder'] ,'0','0' ) )
        ##
        comm_inference = parent.u_info.exec_run_inference[:]

        params = ['--image_size_x', np.str( image_x ), 
                 '--image_size_y', np.str( image_y ),
                 '--image_size_z',  np.str( image_z ),
                 '--parameter_file', config_file
                ]

        comm_inference += params

        print(comm_title)
        # print(comm_inference)
        print('')
        s.run(comm_inference)
        print('')
        print(comm_title, 'was finished.')
        print('')
        return True
        ##


    def SelectMaxModel(self, folder_path):

        required_files = [ \
            'model.ckpt-*.meta', \
            'model.ckpt-*.index',\
            'model.ckpt-*.data-00000-of-00001' ]
        tmp = glob.glob( path.join(folder_path, "*") )
        filenames_in_folder = [os.path.basename(r) for r in tmp]
        cropped = []
        for required_file in required_files:
			#
            tmp = fnmatch.filter(filenames_in_folder, required_file)
            if len(tmp) == 0:
                return False
			#
            a, b = map(len, required_file.split('*'))
            cropped.append( {t[a:-b] for t in tmp} ) 
        intersection = cropped[0] & cropped[1] & cropped[2] 
        if len(intersection) == 0:
            return False
        max_id_name = os.path.join(folder_path, 'model.ckpt-' + str(max(map(int, intersection)))  )
        return max_id_name



    def __init__(self, u_info):
        ##
        datadir = u_info.data_path

#        ffn_file_path        = os.path.join(datadir, "ffn")

#        tensorflow_file      = os.path.join(u_info.tensorflow_model_path, "model.ckpt-2000000")

        self.paramfile = os.path.join(u_info.parameters_path, "FFN_Inference.pickle")

        self.title = 'FFN Inference'

        self.tips = [
                        'Input: Path to folder containing target images.',
                        'Tensorflow model folder. The largest model.ckpt is automatically selected for inference.',
                        'Folder that contains grayscale_maps.h5, groundtruth.h5, and tf_record_file. Inferred segmentation will be stored.',
                        'Click it if you used in the training process.',
                        'Output Checkpoint Interval.'
                        ]

        self.args = [
                        ['Target Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder', 'SelectModelFolder', 'OpenModelFolder'],
                        ['FFNs Folder',   'SelectFFNsFolder', 'OpenFFNsFolder'],
                        ['Sparse Z', 'CheckBox', False],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]]
            ]


