###
###
###
import sys, os, time, errno
import numpy as np
import copy
from itertools import chain
import subprocess as s
import time
import cv2
import h5py
import threading

import contextlib

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
import Miscellaneous as m

#######

#######

from MiscellaneousSegment import MiscellaneousSegment

if getattr(sys, 'frozen', False):
    #print('Run on pyinstaller.')
    exec_run_inference = os.path.join(main_dir, 'run_inference_win.exe')
#
else:
    #print('Run on live python.')
    exec_dir = os.path.join(main_dir, 'segment', '_3D_FFN', 'ffn')
    exec_run_inference = 'python ' + os.path.join(exec_dir, 'run_inference_win.py')

# running live


class FFNInference(MiscellaneousSegment):

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

        ##
        ## h5 file (target image file) generation.
        ##
        target_image_file_h5 = os.path.join(params['FFN File Folder'], "grayscale_inf.h5")

        try:
            target_image_files = self.ObtainImageFiles(params['Target Image Folder'])
            images = [cv2.imread(i, cv2.IMREAD_GRAYSCALE) for i in target_image_files]
            images = np.array(images)
            image_z    = images.shape[0]
            image_y    = images.shape[1]
            image_x    = images.shape[2]
            image_mean = np.mean(images).astype(np.int16)
            image_std  = np.std(images).astype(np.int16)
            print('x: {}, y: {}, z: {}'.format(image_x, image_y, image_z))

            with h5py.File( target_image_file_h5 , 'w') as f:
                f.create_dataset('raw', data=images, compression='gzip')
            print('"grayscale_inf.h5" file (target inference image) was generated.')
        except:
            print("Error: Target Image h5 was not generated.")
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
        request['model_checkpoint_path'] = params['Tensorflow Model Files'].replace('\\', '/')
        request['model_name'] = "convstack_3d.ConvStack3DFFNModel"

        if params['Sparse Z'] != Qt.Unchecked:
            request['model_args'] = "{\\\"depth\\\": 9, \\\"fov_size\\\": [33, 33, 17], \\\"deltas\\\": [8, 8, 4]}"
            #request['model_args'] = ' {"depth":9,"fov_size":[33,33,17],"deltas":[8,8,4]} '
        else :
            request['model_args'] = "{\\\"depth\\\": 12, \\\"fov_size\\\": [33, 33, 33], \\\"deltas\\\": [8, 8, 8]}"
            #request['model_args'] = ' {"depth":12,"fov_size":[33,33,33],"deltas":[8,8,8]} '

        request['segmentation_output_dir'] = params['Output Inference Folder'].replace('\\', '/')
        inference_options = {}
        inference_options['init_activation'] = 0.95
        inference_options['pad_value'] = 0.05
        inference_options['move_threshold'] = 0.9
        inference_options['min_boundary_dist'] = {"x": 1, "y": 1, "z": 1}
        inference_options['segment_threshold'] = 0.6
        inference_options['min_segment_size'] = 1000
        request['inference_options'] = inference_options

        config_file = os.path.join(params['FFN File Folder'], "inference_params.pbtxt")
        with open(config_file, "w", encoding='utf-8') as f:
            self.write_call(f, request, "")

        print('Configuration file was saved at :')
        print(config_file)
        print('\n')
        ##
        ## Inference start (I gave up the use of run_inference because of the augment parsing problem)
        ##
        m.mkdir_safe(os.path.join( params['Output Inference Folder'] ,'0','0' ) )
        ##
        comm_inference = exec_run_inference + ' ' \
                    + ' --image_size_x '  + np.str( image_x ) \
                    + ' --image_size_y '  + np.str( image_y ) \
                    + ' --image_size_z '  + np.str( image_z ) \
                    + ' --parameter_file ' + config_file

        print(comm_title)
        print(comm_inference)
        print('\n')
        s.call(comm_inference)
        print(comm_title, 'was finished.')
        return True
        ##

    def __init__(self, u_info):
        ##
        datadir = u_info.data_path
        Inference_image_path = os.path.join(datadir, "_3DNN_test_images")
        ffn_file_path        = os.path.join(datadir, "ffn")
        tensorflow_file      = os.path.join(datadir, "_3DNN_model_tensorflow", "model.ckpt-2000000")
        self.paramfile = os.path.join(datadir, "parameters", "FFN_Inference.pickle")

        self.filter_name = 'FFN Inference'

        self.tips = [
                        'Path to folder containing target images',
                        'Output inference folder',
                        'Tensorflow model Files. 3 files are required. Please remove their suffixes',
                        'Click it if you used in the training process',
                        'Checkpoint Interval',
                        'Tensorflow file follder'
                        ]

        self.args = [
                        ['Target Image Folder',  'LineEdit', Inference_image_path, 'BrowseDirImg'],
                        ['Output Inference Folder',  'LineEdit', ffn_file_path, 'BrowseDir'],
                        ['Tensorflow Model Files', 'LineEdit', tensorflow_file, 'BrowseFile'],
                        ['Sparse Z', 'CheckBox', False],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['FFN File Folder', 'LineEdit', ffn_file_path, 'BrowseDir']
            ]


    def Execute(self, parent, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)

        removal_file1 = os.path.join( params['Output Inference Folder'] ,'0','0','seg-0_0_0.npz' )
        removal_file2 = os.path.join( params['Output Inference Folder'], '0','0','seg-0_0_0.prob')

        if os.path.isfile(removal_file1) or os.path.isfile(removal_file2) :
            Reply = QMessageBox.question(parent, 'FFN', 'seg-0_0_0 files were found at the Output Inference Folder. Remove them?',  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if Reply == QMessageBox.Yes:
                with contextlib.suppress(FileNotFoundError):
                    os.remove(removal_file1)
                with contextlib.suppress(FileNotFoundError):
                    os.remove(removal_file2)
                print('seg-0_0_0 files were removed.')
            else:
                print('FFN inference was canceled.')
                return

        thread = threading.Thread(target=self._Run, args=( parent, params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent, 'FFN',  comm_title + ' runs on a different process.')
        # parent.close()
        return

