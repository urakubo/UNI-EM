###
###
###
import sys, os, time, errno
import subprocess as s
import glob
import cv2
import numpy as np
from os import path, pardir
import shutil

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))
import miscellaneous.Miscellaneous as m


class InferenceExe():

    def _Run(self, parent, params, comm_title):

        datadir = parent.u_info.data_path

        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        input_png = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        input_tif = glob.glob(os.path.join(params['Image Folder'], "*.tif"))
        input_files.extend(input_png)
        input_files.extend(input_tif)
        if len(input_files) == 0:
            print('No images in the Image Folder.')
            return

        im = m.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('')
        print('Target file to check color type : ', input_files[0])
        print('Image dimensions                : ', im.shape)
        print('Image filetype                  : ', im.dtype)
        image_size_x = im.shape[1]
        image_size_y = im.shape[0]
        converted_size_x = image_size_x
        converted_size_y = image_size_y
        std_sizes = [2 ** i for i in range(8, 15)] # 256, 512, ..., 16384
        np_std_sizes = np.array(std_sizes)

        if ( image_size_x > max(std_sizes) or image_size_y > max(std_sizes) ):
            print('Image size is too big.')
            return
        if ( image_size_x < min(std_sizes) or image_size_y < min(std_sizes) ):
            print('Image size is too small.')
            return

        # Generate tmpdir
        tmpdir = os.path.join(params['Output Segmentation Folder'], "standardized_images")
        if os.path.exists(tmpdir) :
            shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)

        ##
        ## Check whether the target images should be converted.
        ##
        if not (im.dtype == "uint8" and len(im.shape) == 3 and input_tif == [] and
                image_size_x in std_sizes and image_size_y in std_sizes) :

            # Check image size
            converted_size_x_id = np.min( np.where((np_std_sizes - image_size_x) > 0) )
            converted_size_y_id = np.min( np.where((np_std_sizes - image_size_y) > 0) )
            converted_size_x    = np_std_sizes[converted_size_x_id]
            converted_size_y    = np_std_sizes[converted_size_y_id]
            fringe_size_x = converted_size_x - image_size_x
            fringe_size_y = converted_size_y - image_size_y

            # Image Conversion
            for input_file in input_files:
                im_col = m.imread(input_file)
                filename = path.basename(input_file)
                filename = filename.replace('.tif', '.png')
                converted_filename = os.path.join( tmpdir, filename )

                # add fringe X
                im_fringe_x = cv2.flip(im_col, 1) # flipcode > 0, left-right
                im_fringe_x = im_fringe_x[ :, 0:fringe_size_x]
                converted_image = cv2.hconcat([im_col, im_fringe_x])
                # add fringe Y
                im_fringe_y = cv2.flip(converted_image, 0) # flipcode = 0, top-bottom
                im_fringe_y = im_fringe_y[0:fringe_size_y, :]
                converted_image = cv2.vconcat([converted_image, im_fringe_y])
                # Save
                m.imwrite(converted_filename, converted_image)

            #Complete
            params['Image Folder'] = tmpdir
            print('Filetype of images was changed to RGB 8bit, and stored in ', tmpdir)


        tmp = ['--mode'		, 'predict'	,\
        	'--save_freq'	, '0'		,\
        	'--input_dir'	, params['Image Folder'], \
			'--output_dir'	, params['Output Segmentation Folder'], \
			'--checkpoint'	, params['Model Folder'], \
            '--image_height', str(converted_size_y), \
            '--image_width'	, str(converted_size_x)]

        comm = parent.u_info.exec_translate
        comm.extend( tmp )

        try:
            print('')
            print('  '.join(comm))
            print('')
            print('Start inference.')
            m.UnlockFolder(parent.u_info, params['Output Segmentation Folder'])  # Only for shared folder/file
            s.call(comm)
            ## Cut out fringes
            output_files = glob.glob(os.path.join(params['Output Segmentation Folder'], "*.jpg"))
            output_png   = glob.glob(os.path.join(params['Output Segmentation Folder'], "*.png"))
            output_tif   = glob.glob(os.path.join(params['Output Segmentation Folder'], "*.tif"))
            output_files.extend(output_png)
            output_files.extend(output_tif)
            for output_file in output_files:
                im_col = m.imread(output_file)
                im_col = im_col[0:image_size_y, 0:image_size_x]
                m.imwrite(output_file, im_col)
            ##

        except s.CalledProcessError as e:
            print("Inference was not executed.")
            if os.path.exists(tmpdir) :
                shutil.rmtree(tmpdir)
            m.LockFolder(parent.u_info, params['Output Segmentation Folder'])
            return

		# rm tmpdir
        if os.path.exists(tmpdir) :
            shutil.rmtree(tmpdir)

        m.LockFolder(parent.u_info, params['Output Segmentation Folder'])
        return
