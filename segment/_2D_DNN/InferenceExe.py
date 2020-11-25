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
import threading

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))
import miscellaneous.Miscellaneous as m


class InferenceExe():

    def _Run(self, parent, params, comm_title):


        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        input_png = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        input_tif = glob.glob(os.path.join(params['Image Folder'], "*.tif"))
        input_files.extend(input_png)
        input_files.extend(input_tif)
        if len(input_files) == 0:
            print('No images in the Image Folder.')
            return False
        im = m.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        root, ext_image = os.path.splitext(os.path.basename(input_files[0]))

        print('')
        print('Target file to check color type : ', input_files[0])
        print('Image dimensions                : ', im.shape)
        print('Image filetype                  : ', im.dtype)
        image_size_x = im.shape[1]
        image_size_y = im.shape[0]

        if ( image_size_x <= 256 or image_size_y <= 256 ):
            print('Image size is too small.')
            return False


        # Generate tmpdir
        tmpdir_standardized = os.path.join(params['Output Segmentation Folder (Empty)'], "standardized"+str(threading.get_ident()).zfill(6)[-6:] )
        if os.path.exists(tmpdir_standardized) :
            shutil.rmtree(tmpdir_standardized)
        os.mkdir(tmpdir_standardized)
        #
        tmpdir_output = os.path.join(params['Output Segmentation Folder (Empty)'], "output"+str(threading.get_ident()).zfill(6)[-6:] )
        if os.path.exists(tmpdir_output) :
            shutil.rmtree(tmpdir_output)
        os.mkdir(tmpdir_output)


        ## Check image size
        max_image_size = params['Maximal unit image size']
        if max_image_size == '512' :
            std_sizes = np.array([512])
        elif max_image_size == '1024' :
            std_sizes = np.array([512, 1024])
        elif max_image_size == '2048' :
            std_sizes = np.array([512, 1024, 2048])
        else :
            print('Internal error at Maximal unit image size.')
            return False

        max_std_size = np.max(std_sizes)
        if image_size_x > max_std_size :
        	unit_image_size_x = max_std_size
        	num_tiles_x      = np.int( np.ceil( float( image_size_x ) / max_std_size  ) )
        else:
        	unit_image_size_x = np.min(std_sizes[std_sizes>=image_size_x])
        	num_tiles_x      = 1

        if image_size_y > max_std_size :
        	unit_image_size_y = max_std_size
        	num_tiles_y      = np.int( np.ceil( float( image_size_y ) / max_std_size  ) )
        else:
        	unit_image_size_y = np.min(std_sizes[std_sizes>=image_size_y])
        	num_tiles_y      = 1
		#
        converted_size_x = unit_image_size_x * num_tiles_x
        converted_size_y = unit_image_size_y * num_tiles_y
        fringe_size_x = converted_size_x - image_size_x
        fringe_size_y = converted_size_y - image_size_y

		#
		#
        output_files = []
        print('Image standardization: ')
        for input_file in input_files:
            im_col = m.imread(input_file)
            # im_col = self._ChangeIntoColor(im_col)

            filename = path.basename(input_file)
            print(filename+' ')
            filename = filename.replace('.tif', '.png')
            output_files.append(filename)

            # add fringe X
            im_fringe_x = cv2.flip(im_col, 1) # flipcode > 0, left-right
            im_fringe_x = im_fringe_x[ :, 0:fringe_size_x]
            converted_image = cv2.hconcat([im_col, im_fringe_x])
            # add fringe Y
            im_fringe_y = cv2.flip(converted_image, 0) # flipcode = 0, top-bottom
            im_fringe_y = im_fringe_y[0:fringe_size_y, :]
            converted_image = cv2.vconcat([converted_image, im_fringe_y])
            # Save
            if (num_tiles_x == 1) and (num_tiles_y == 1) :
            	converted_filename = os.path.join( tmpdir_standardized, filename )
            	m.imwrite(converted_filename, converted_image)
            else :
            	for iy in range( num_tiles_y ):
            		for ix in range( num_tiles_x ):
            			y0 = iy * unit_image_size_y
            			y1 = y0 + unit_image_size_y
            			x0 = ix * unit_image_size_x
            			x1 = x0 + unit_image_size_x
            			current_tile = converted_image[y0:y1, x0:x1]
            			converted_filename = str(ix).zfill(3)[-3:]+'_'+ str(iy).zfill(3)[-3:]+'_'+filename
            			converted_filename = os.path.join( tmpdir_standardized, converted_filename )
            			m.imwrite(converted_filename, current_tile)

        #Complete
        print('')
        print('Images were split and changed into RGB 8bit, and stored in ', tmpdir_standardized)
        print('')

        tmp = ['--mode'		, 'predict'	, \
        	'--save_freq'	, '0'		, \
        	'--input_dir'	, tmpdir_standardized, \
			'--output_dir'	, tmpdir_output, \
			'--checkpoint'	, params['Model Folder'], \
            '--image_height', str(unit_image_size_y), \
            '--image_width'	, str(unit_image_size_x)]

        comm = parent.u_info.exec_translate[:]
        comm.extend( tmp )


        print('')
        print('  '.join(comm))
        print('')
        print('Start inference.')
        print('')
        m.UnlockFolder(parent.u_info, params['Output Segmentation Folder (Empty)'])  # Only for shared folder/file
        s.run(comm)

        print('Segmentation reconstruction: ')
        for output_file in output_files:
			##
        	print(output_file, ' ')
        	if (num_tiles_x == 1) and (num_tiles_y == 1) :
        	## Remove fringes
        		filename = os.path.join( tmpdir_output, output_file )
        		inferred_segmentation = m.imread(filename)
        	else :
        	## Merge split images.
        		inferred_segmentation = np.zeros((converted_size_y, converted_size_x, 3), dtype = int)
        		for iy in range( num_tiles_y ):
	        		for ix in range( num_tiles_x ):
	        			y0 = iy * unit_image_size_y
	        			y1 = y0 + unit_image_size_y
	        			x0 = ix * unit_image_size_x
	        			x1 = x0 + unit_image_size_x
	        			current_tile_filename = str(ix).zfill(3)[-3:]+'_'+ str(iy).zfill(3)[-3:]+'_'+output_file
	        			current_tile_filename = os.path.join( tmpdir_output, current_tile_filename )
	        			current_tile = m.imread(current_tile_filename)
	        			inferred_segmentation[y0:y1, x0:x1] = current_tile
        	inferred_segmentation = inferred_segmentation[0:image_size_y, 0:image_size_x]

        	filename = os.path.splitext(os.path.basename(output_file))[0] + ext_image
        	filename = os.path.join( params['Output Segmentation Folder (Empty)'], filename )
        	m.imwrite(filename, inferred_segmentation)

        ##

		# rm tmpdir
        if os.path.exists(tmpdir_standardized) :
            shutil.rmtree(tmpdir_standardized)
        if os.path.exists(tmpdir_output) :
            shutil.rmtree(tmpdir_output)

        parent.parent.ExecuteCloseFileFolder(params['Output Segmentation Folder (Empty)'])
        parent.parent.OpenFolder(params['Output Segmentation Folder (Empty)'])
        print('')
        print('Finish inference.')
        print('')
        return True


    def _ChangeIntoColor(self, img):

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

               

