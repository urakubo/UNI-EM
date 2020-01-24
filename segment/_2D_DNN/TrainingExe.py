##
##
##

import sys, os, time, errno
import glob
import cv2
import shutil
import subprocess as s
from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
##
##
##

class TrainingExe():

    def _Run(self, parent, params, comm_title):

        datadir = parent.u_info.data_path

        ##
        ## Check bitdepth of EM images and segmentation in the target directory.
        ## Translate.py only accepts unit24 (RGB color).
        ##
        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        input_png = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        input_tif = glob.glob(os.path.join(params['Image Folder'], "*.tif"))
        input_files.extend(input_png)
        input_files.extend(input_tif)
        im = cv2.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('Target file to check color type : ', input_files[0])
        print('Image dimensions                : ', im.shape)
        print('Image filetype                  : ', im.dtype)
        if not (im.dtype == "uint8" and len(im.shape) == 3 and input_tif == []) :
            tmpdir = os.path.join(datadir, "tmp", "DNN_training_images")
            if os.path.exists(tmpdir) :
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            for input_file in input_files:
                im_col = cv2.imread(input_file)
                filename = os.path.basename(input_file)
                filename = filename.replace('.tif', '.png')
                converted_input_file = os.path.join( tmpdir, filename )
                cv2.imwrite(converted_input_file, im_col)
            params['Image Folder'] = tmpdir
            print('Filetype of images was changed to RGB 8bit, and stored in ', tmpdir)

        ##
        ## Check and change filetype of input segmentation
        ##
        input_files = glob.glob(os.path.join(params['Segmentation Folder'], "*.jpg"))
        input_png = glob.glob(os.path.join(params['Segmentation Folder'], "*.png"))
        input_tif = glob.glob(os.path.join(params['Segmentation Folder'], "*.tif"))
        input_files.extend(input_png)
        input_files.extend(input_tif)

        im = cv2.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('Target file to check color type : ', input_files[0])
        print('Segmentation image dimensions   : ', im.shape)
        print('Segmentation filetype           : ', im.dtype)
        if not (im.dtype == "uint8" and len(im.shape) == 3 and input_tif == []) :
            tmpdir = os.path.join(datadir, "tmp", "DNN_ground_truth")
            if os.path.exists(tmpdir) :
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            for input_file in input_files:
                im_col = cv2.imread(input_file)
                filename = os.path.basename(input_file)
                filename = filename.replace('.tif', '.png')
                converted_input_file = os.path.join( tmpdir, filename )
                cv2.imwrite(converted_input_file, im_col)
            params['Segmentation Folder'] = tmpdir
            print('Filetype of segmentation was changed to RGB 8bit, and stored in', tmpdir)


        #
        # Dialog to specify directory
        #

        aug = params['Augmentation']
        if   aug == "fliplr, flipud, transpose":
            augmentation = '--fliplr --flipud --transpose'
        elif aug == "fliplr, flipud":
            augmentation = '--fliplr --flipud --no_transpose'
        elif aug == "fliplr":
            augmentation = '--fliplr --no_flipud --no_transpose'
        elif aug == "flipud":
            augmentation = '--no_fliplr --flipud --no_transpose'
        elif aug == "None":
            augmentation = '--no_fliplr --no_flipud --no_transpose'
        else :
            print("Internal error at Augumentation of PartDialogTrainingExecutor.")
            self._Cancel()
            return
        #
        #   ' --model ' + params['Model'] + ' '
        #

        comm = parent.u_info.exec_translate +' ' \
                + ' --mode train ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
                + ' --target_dir ' + params['Segmentation Folder'] + ' ' \
                + ' --output_dir ' + params['Model Folder'] + ' ' \
                + ' --loss ' + params['Loss Function'] + ' ' \
                + ' --network ' + params['Network'] + ' ' \
                + ' ' + augmentation + ' ' \
                + ' --max_epochs ' + params['Maximal Epochs'] + ' ' \
                + ' --display_freq ' +  params['Display Frequency'] + ' ' \
                + ' --u_depth ' + params['U depth'] + ' ' \
                + ' --n_res_blocks ' + params['N res blocks'] + ' ' \
                + ' --n_highway_units ' + params['N highway units'] + ' ' \
                + ' --n_dense_blocks ' + params['N dense blocks'] + ' ' \
                + ' --n_dense_layers ' + params['N dense layers'] + ' '


        print(comm)
        print('Start training.')
        try:
            s.call(comm.split())
        except s.CalledProcessError as e:
            print("Error ocurrs in Traslate.py.")
            return

        return


