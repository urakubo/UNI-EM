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
# import threading

from PyQt5.QtWidgets import QMessageBox

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
import miscellaneous.Miscellaneous as m

icon_dir = path.join(main_dir, "icons")
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))


class FFNPrepTraining():

    def _Run(self, parent, params, comm_title):
        ##
        comm_compute_partition = parent.u_info.exec_compute_partition +' ' \
                + ' --input_volume '  + os.path.join(params['FFN File Folder'], "groundtruth.h5@stack")  + ' ' \
                + ' --output_volume ' + os.path.join(params['FFN File Folder'], "af.h5@af") + ' ' \
                + ' --thresholds 0.025,0.05,0.075,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9 ' \
                + ' --lom_radius 24,24,24 ' \
                + ' --min_size 10000 '

        comm_build_coordinates = parent.u_info.exec_build_coordinates +' ' \
                + ' --partition_volumes validation1@'  +  os.path.join(params['FFN File Folder'], "af.h5@af")  + ' ' \
                + ' --coordinate_output ' + os.path.join(params['FFN File Folder'], "tf_record_file") + ' ' \
                + ' --margin 24,24,24 '
        ##
        # try:
        ##
        training_image_files = m.ObtainImageFiles(params['Training Image Folder'])
        images = [m.imread(i, cv2.IMREAD_GRAYSCALE) for i in training_image_files]
        images = np.array(images)
        with h5py.File(os.path.join(params['FFN File Folder'], "grayscale_maps.h5"), 'w') as f:
            f.create_dataset('raw', data=images, compression='gzip')
        print('"grayscale_maps.h5" file (training image) was generated.')

        ground_truth_files = m.ObtainImageFiles(params['Ground Truth Folder'])
        images = [m.imread(i, cv2.IMREAD_UNCHANGED) for i in ground_truth_files]
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

        processed_file_path   = os.path.join(datadir, "ffn")

        self.paramfile = os.path.join(u_info.parameters_path, "FFN_PrepTraining.pickle")

        self.title = 'FFN Preparation'

        self.tips = [
                        'Input: Path to folder containing images',
                        'Input: Path to folder containing ground truth',
                        'Output: Tensorflow file folder'
                        ]


        self.args = [
                        ['Training Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Ground Truth Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['FFN File Folder',   'LineEdit', processed_file_path, 'BrowseDir'],
            ]



