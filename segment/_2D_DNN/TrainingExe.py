##
##
##

import sys, os, time, errno
import glob
import cv2
import shutil
import subprocess as s
import numpy as np
import threading
from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
import miscellaneous.Miscellaneous as m
##
##
##

class TrainingExe():

    def _Run(self, parent, params, comm_title):
        ##
        ## Transform bitdepth of EM images and segmentation in the target directory.
        ## Translate.py only accepts unit24 (RGB color).
        ##
        img_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        img_png = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        img_tif = glob.glob(os.path.join(params['Image Folder'], "*.tif"))
        img_files.extend(img_png)
        img_files.extend(img_tif)
        if len(img_files) == 0:
            print('No image file.')
            return

        im = m.imread(img_files[0], cv2.IMREAD_UNCHANGED)
        print('')
        print('Number of images : ', len(img_files))
        print('Image color type : ', img_files[0])
        print('Image dimensions : ', im.shape)
        print('Image filetype   : ', im.dtype)

        seg_files = glob.glob(os.path.join(params['Segmentation Folder'], "*.jpg"))
        seg_png = glob.glob(os.path.join(params['Segmentation Folder'], "*.png"))
        seg_tif = glob.glob(os.path.join(params['Segmentation Folder'], "*.tif"))
        seg_files.extend(seg_png)
        seg_files.extend(seg_tif)
        if len(seg_files) == 0:
            print('')
            print('No segmentation file.')
            print('Aborted.')
            return

        sg = m.imread(seg_files[0], cv2.IMREAD_UNCHANGED)
        print('')
        print('Number of Segmentation images : ', len(seg_files))
        print('Segmentation color type       : ', seg_files[0])
        print('Segmentation image dimensions : ', sg.shape)
        print('Segmentation filetype         : ', sg.dtype)
        print('')

        if len(img_files) != len(seg_files):
            print('The number of images is not equal to that of segmenation images.')
            print('Aborted.')
            return


		# Generate tmpdir
        tmpdir = os.path.join( params['Model Folder (Empty)'], "paired"+str(threading.get_ident()).zfill(6)[-6:] ) #  )
        if os.path.exists(tmpdir) :
            shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)

        for img_file, seg_file in zip(img_files, seg_files):

            img = m.imread(img_file)
            seg = m.imread(seg_file)

            img = np.array(img, dtype=np.uint8)
            seg = np.array(seg, dtype=np.uint8)

            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            elif img.shape[2] != 3:
                print('File is broken: ', img_file)
                print('Aborted.')
                return

            if len(seg.shape) == 2:
                seg = cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR)
            elif seg.shape[2] == 4:
                seg = cv2.cvtColor(seg, cv2.COLOR_BGRA2BGR)
            elif seg.shape[2] != 3:
                print('File is broken: ', seg_file)
                print('Aborted.')
                return

            paired = cv2.hconcat([img, seg])

            tmpname = os.path.splitext(os.path.basename(img_file))[0]
            filename_paired = os.path.join( tmpdir, tmpname + '.png' )
            m.imwrite(filename_paired, paired)

        print('Paired images (RGB 8bit) are stored in ', tmpdir)
        print('')

        #
        # Dialog to specify directory
        #

        aug = params['Augmentation']
        if   aug == "fliplr, flipud, transpose":
            augmentation = ['--fliplr', '--flipud', '--transpose']
        elif aug == "fliplr, flipud":
            augmentation = ['--fliplr', '--flipud', '--no_transpose']
        elif aug == "fliplr":
            augmentation = ['--fliplr', '--no_flipud', '--no_transpose']
        elif aug == "flipud":
            augmentation = ['--no_fliplr', '--flipud', '--no_transpose']
        elif aug == "None":
            augmentation = ['--no_fliplr', '--no_flipud', '--no_transpose']
        else :
            print("Internal error at Augumentation of PartDialogTrainingExecutor.")
            self._Cancel()
            return
        #
        #   ' --model ' + params['Model'] + ' '
        #
 		# parent.u_info.exec_translate, \
 
        tmp = ['--batch_size'		, '4', \
            '--mode'			, 'train', \
			'--input_dir'		, tmpdir, \
			'--output_dir'		, params['Model Folder (Empty)'], \
            '--loss'			, params['Loss Function'], \
			'--network'		, params['Network'], \
        	'--max_epochs'		, str( params['Maximal Epochs']  ),  \
        	'--display_freq'	, str( params['Display Frequency'] ),  \
        	'--u_depth'		, str( params['U depth'] ),  \
        	'--n_res_blocks'	, str( params['N res blocks'] ), \
        	'--n_highway_units', str( params['N highway units'] ), \
        	'--n_dense_blocks'	, str( params['N dense blocks'] ), \
        	'--n_dense_layers'	, str( params['N dense layers']) ]

        comm = parent.u_info.exec_translate[:]
        comm.extend( tmp )
        comm.extend( augmentation )

        print('')
        print('  '.join(comm))
        print('')
        print('Start training.')
        print('')
        m.UnlockFolder(parent.u_info,  params['Model Folder (Empty)'])
        s.run(comm)
        # rm tmpdir
        if os.path.exists(tmpdir) :
        	shutil.rmtree(tmpdir)
        m.LockFolder(parent.u_info,  params['Model Folder (Empty)'])
        parent.parent.ExecuteCloseFileFolder(params['Model Folder (Empty)'])
        parent.parent.OpenFolder(params['Model Folder (Empty)'])
        print('')
        print('Finish training.')
        print('')

        return


