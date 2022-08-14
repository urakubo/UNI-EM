##
##
##
import sys, os
import subprocess as s
import miscellaneous.Miscellaneous as m
from PyQt5.QtCore import Qt

import os, sys, shutil, pprint, math
import numpy as np
import json
from itertools import product
#import cv2
#from tifffile import imread


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
# exec_template = ['python', os.path.join(main_dir, 'plugins', 'Template', 'run_example.py')]



def _check_image_attr(input_file):
	ext = os.path.splitext(os.path.basename(input_file))[1][1:]
	im = m.read_image(input_file, ext)
	print('Target image file: ', input_file)
	print('ext              : ', ext )
	print('Image dimension  : ', im.shape)
	print('Image filetype   : ', im.dtype)
	return ext, im.shape, im.dtype



def _create_output_folders( params, num_h, num_w, num_z ):

	'''
	if os.path.exists( params['Split img/seg folder (Empty)'] ):
		question = 'Split img/seg folder "{}" already exists. Remove it?'.format(params['Split img/seg folder'])
		reply = m.query_yes_no(question, default="yes")
		if reply == True:
			shutil.rmtree(params['Split img/seg folder (Empty)'])
		else:
			exit()
	'''

	os.makedirs(params['Split img/seg folder (Empty)'], exist_ok=True)
	hs = range( num_h )
	ws = range( num_w )
	zs = range( num_z )
	for ih, iw, iz  in product(hs, ws, zs):
		folder_name = '{:03d}_{:03d}_{:03d}'.format(ih,iw,iz)
		output_folder = os.path.join(params['Split img/seg folder (Empty)'], \
			params['Img folder'], folder_name )
		os.makedirs(output_folder, exist_ok=True)
		if params['Seg folder'] != '':
			output_folder = os.path.join(params['Split img/seg folder (Empty)'], \
				params['Seg folder'], folder_name )
			os.makedirs(output_folder, exist_ok=True)
	return True



class Splitter():

	def _Run(self, parent, params, comm_title):
		#
		original_image_files = m.obtain_list_image_files( params['Target image folder'] )
		ext, im_shape, im_dtype = _check_image_attr(original_image_files[0])
		
		params['Img folder'] = 'img'
		params['Seg folder'] = 'seg'
		
		split_size_h   = int(params['Split size (h)'])
		split_size_w   = int(params['Split size (w)'])
		split_size_z   = int(params['Split size (z)'])
		
		overlap_size_h = int(params['Overlap size (h, even number)'])
		overlap_size_w = int(params['Overlap size (w, even number)'])
		overlap_size_z = int(params['Overlap size (z, even number)'])
		
		if   overlap_size_h % 2 != 0:
			print('Overlap size (h) is not a even number.')
			return False
		elif overlap_size_w % 2 != 0:
			print('Overlap size (w) is not a even number.')
			return False
		elif overlap_size_z % 2 != 0:
			print('Overlap size (z) is not a even number.')
			return False
		
		if   overlap_size_h >= split_size_h:
			print('Overlap size (h) must be smaller than Split size (h).')
			return False
		elif overlap_size_w >= split_size_w:
			print('Overlap size (w) must be smaller than Split size (w).')
			return False
		elif overlap_size_z >= split_size_z:
			print('Overlap size (z) must be smaller than Split size (z).')
			return False
		
		
		im_size_h = im_shape[0]
		im_size_w = im_shape[1]
		im_size_z = len(original_image_files)
		ids_original_files = list(range(im_size_z))
		
			
		if params['Reflect padding'] != Qt.Unchecked:
			im_size_h += 2*overlap_size_h
			im_size_w += 2*overlap_size_w
			im_size_z += 2*overlap_size_z

		im_split_size    = list(im_shape)
		im_split_size[0] = split_size_h
		im_split_size[1] = split_size_w

		cropped_hs, num_h = m.crop_with_overlap(im_size_h, split_size_h, overlap_size_h)
		cropped_ws, num_w = m.crop_with_overlap(im_size_w, split_size_w, overlap_size_w)
		cropped_zs, num_z = m.crop_with_overlap(im_size_z, split_size_z, overlap_size_z)
		print('num_h ', num_h)
		print('num_w ', num_w)
		print('num_z ', num_z)

		if params['Reflect padding'] != Qt.Unchecked:
			ids_original_files =  ids_original_files[overlap_size_z:0:-1] \
					+ ids_original_files \
					+ ids_original_files[-2:-2-overlap_size_z:-1]

		if len(im_shape) == 3:
			pad_width = ((overlap_size_h, overlap_size_h), (overlap_size_w, overlap_size_w), (0, 0))
		else:
			pad_width = ((overlap_size_h, overlap_size_h), (overlap_size_w, overlap_size_w))

		#
		_create_output_folders(params, num_h, num_w, num_z  )

		ids_original_files = [ids_original_files[z[0]:z[1]] for z in cropped_zs]
		z_info = []
		for iz in  range( num_z ):
			z_sub_info = []
			for i_slice, id_original_file in enumerate( ids_original_files[iz] ):
				image_file = original_image_files[id_original_file]
				z_sub_info.append({'i_slice': i_slice, 'id_original_file': id_original_file, 'image_file': image_file})
				print('image_file: ', image_file)
				image = m.read_image(image_file, ext)
				
				if params['Reflect padding'] != Qt.Unchecked:
					image = np.pad(image, pad_width=pad_width, mode='reflect')

				for ih, iw in product( range(num_h), range(num_w) ):
					h = cropped_hs[ih]
					w = cropped_ws[iw]
					if h[1]-h[0] < split_size_h or w[1]-w[0] < split_size_w:
						cropped_image = np.zeros(im_split_size, dtype=im_dtype)
						cropped_image[0:h[1]-h[0], 0:w[1]-w[0]] = image[h[0]:h[1], w[0]:w[1]]
					else:
						cropped_image = image[h[0]:h[1], w[0]:w[1]]
						
					output_file = os.path.join(params['Split img/seg folder (Empty)'], \
						params['Img folder'], \
						'{:03d}_{:03d}_{:03d}'.format(ih,iw,iz), '{:04d}.{}'.format( i_slice, ext ) )
					m.imwrite(output_file, cropped_image)
			z_info.append(z_sub_info)

		# Save data
		
		p ={}
		if params['Reflect padding'] != Qt.Unchecked:
			p['Reflect padding'] = True
		else:
			p['Reflect padding'] = False
		
		p['Img folder'] = params['Img folder']
		p['Seg folder'] = params['Seg folder']

		p['im_size_h'] = im_size_h
		p['im_size_w'] = im_size_w
		p['im_size_z'] = im_size_z
		p['cropped_hs'] = cropped_hs
		p['cropped_ws'] = cropped_ws
		p['cropped_zs'] = cropped_zs
		p['num_h'] = num_h
		p['num_w'] = num_w
		p['num_z'] = num_z
		p['ext']   = ext
		p['im_dtype']   = str(im_dtype)
		p['im_shape']   = im_shape
		p['z_info']     = z_info

		p['Split size (h)']= params['Split size (h)']
		p['Split size (w)']= params['Split size (w)']
		p['Split size (z)']= params['Split size (z)']

		p['Overlap size (h)']= params['Overlap size (h, even number)']
		p['Overlap size (w)']= params['Overlap size (w, even number)']
		p['Overlap size (z)']= params['Overlap size (z, even number)']


		filename = os.path.join(params['Split img/seg folder (Empty)'], 'attr.json')
		with open(filename, 'w') as fp:
			json.dump(p, fp, indent=4)
		
		
		#
		print(comm_title, 'was finished.')
		return True

	def __init__(self, u_info):
		##
		self.u_info = u_info
		self.paramfile = os.path.join(u_info.parameters_path, "Splitter.pickle")

		self.title = 'Splitter'

		self.tips = [
		                'Target image folder',
		                'Split img/seg folder (Empty)',
		                'Split size of the target volume image (h)',
		                'Split size of the target volume image (w)',
		                'Split size of the target volume image (z)',
		                'Size of the margin for connection (h)',
		                'Size of the margin for connection (w)',
		                'Size of the margin for connection (z)',
						'Reflect center padding for fringe extension'
		                ]

		self.args = [
		                ['Target image folder', 'SelectImageFolder', 'OpenImageFolder'],
		                ['Split img/seg folder (Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder'],
		                ['Split size (h)', 'SpinBox', [2, 1024, 32768]],
		                ['Split size (w)', 'SpinBox', [2, 1024, 32768]],
		                ['Split size (z)', 'SpinBox', [2, 100 , 32768]],
		                ['Overlap size (h, even number)', 'SpinBox', [2, 24, 255]],
		                ['Overlap size (w, even number)', 'SpinBox', [2, 24, 255]],
		                ['Overlap size (z, even number)', 'SpinBox', [2, 4, 255]],
		                ['Reflect padding', 'CheckBox', False]
		    ]


