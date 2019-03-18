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

from PyQt5.QtWidgets import QMessageBox

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))

from MiscellaneousSegment import MiscellaneousSegment

if getattr(sys, 'frozen', False):
    #print('Run on pyinstaller.')
    exec_compute_partition = os.path.join(main_dir, 'compute_partitions.exe')
    exec_build_coordinates = os.path.join(main_dir, 'build_coordinates.exe')
# running in a bundle
else:
    #print('Run on live python.')
    exec_dir = os.path.join(main_dir, 'segment', '_3D_FFN', 'ffn')
    exec_compute_partition = 'python ' +  os.path.join(exec_dir, 'compute_partitions.py')
    exec_build_coordinates = 'python ' +  os.path.join(exec_dir, 'build_coordinates.py')
# running live


class FFNPrepTraining(MiscellaneousSegment):

    def _Run(self, parent, params, comm_title):
        ##
        comm_compute_partition = exec_compute_partition +' ' \
                + ' --input_volume '  + os.path.join(params['FFN File Folder'], "groundtruth.h5@stack")  + ' ' \
                + ' --output_volume ' + os.path.join(params['FFN File Folder'], "af.h5@af") + ' ' \
                + ' --thresholds 0.025,0.05,0.075,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9 ' \
                + ' --lom_radius 24,24,24 ' \
                + ' --min_size 10000 '

        comm_build_coordinates = exec_build_coordinates +' ' \
                + ' --partition_volumes validation1@'  +  os.path.join(params['FFN File Folder'], "af.h5@af")  + ' ' \
                + ' --coordinate_output ' + os.path.join(params['FFN File Folder'], "tf_record_file") + ' ' \
                + ' --margin 24,24,24 '
        ##
        # try:
        training_image_files = self.ObtainImageFiles(params['Training Image Folder'])
        images = [cv2.imread(i, cv2.IMREAD_GRAYSCALE) for i in training_image_files]
        images = np.array(images)
        with h5py.File(os.path.join(params['FFN File Folder'], "grayscale_maps.h5"), 'w') as f:
            f.create_dataset('raw', data=images, compression='gzip')
        print('"grayscale_maps.h5" file (training image) was generated.')

        ground_truth_files = self.ObtainImageFiles(params['Ground Truth Folder'])
        images = [cv2.imread(i, -1) for i in ground_truth_files]
        images = np.array(images).astype(np.int32)
        with h5py.File(os.path.join(params['FFN File Folder'], "groundtruth.h5"), 'w') as f:
            f.create_dataset('stack', data=images, compression='gzip')
        print('"groundtruth.h5" file (ground truth) was generated.')
        ##
        #except:
        #    print("Error: h5 files (ground truth) were not generated.")
        #    return False
        ##
        try:
            print(comm_title)
            print('Start compute_partitions.')
            print(comm_compute_partition)
            s.run(comm_compute_partition.split())
            print('Start build_coordinates.')
            print(comm_build_coordinates)
            s.run(comm_build_coordinates.split())
            print(comm_title, 'was finished.')
        ##
        except :
            print("Error: ", comm_title, " was not executed.")
            return False
        ##
        return True
        ##

    def __init__(self, u_info):
        ##
        datadir = u_info.data_path
        training_image_path = os.path.join(datadir, "_3DNN_training_images")
        ground_truth_path   = os.path.join(datadir, "_3DNN_ground_truth")
        processed_file_path   = os.path.join(datadir, "ffn")
        self.paramfile = os.path.join(datadir, "parameters", "FFN_PrepTraining.pickle")

        self.filter_name = 'FFN Preparation'

        self.tips = [
                        'Path to folder containing images',
                        'Path to folder containing ground truth',
                        'Tensorflow file follder'
                        ]


        self.args = [
                        ['Training Image Folder',  'LineEdit', training_image_path, 'BrowseDirImg'],
                        ['Ground Truth Folder',     'LineEdit', ground_truth_path, 'BrowseDirImg'],
                        ['FFN File Folder',   'LineEdit', processed_file_path, 'BrowseDir'],
            ]


    def Execute(self, parent, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)
        thread = threading.Thread(target=self._Run, args=( parent, params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent, 'FFN',  comm_title + ' runs on a different process.')
        # parent.close()
        return

