##
##
##
import sys, os
import subprocess as s
import miscellaneous.Miscellaneous as m

import os, sys, shutil, pprint
import numpy as np
import json
from itertools import product


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main


def _create_folder_merge( params ):

	if os.path.exists( params['Merged segmentation folder'] ):
		question = 'Merged segmentation folder "{}" already exists. Remove it?'.format(params['Merged segmentation folder'])
		reply = m.query_yes_no(question, default="yes")
		if reply == True:
			shutil.rmtree(params['Merged segmentation folder'])
		else:
			exit()

	os.makedirs(params['Merged segmentation folder'], exist_ok=True)
	return True


def _obtain_seg_dir(params,ih,iw,iz):
	return os.path.join(params['Split img/seg folder'], params['Seg folder'], '{:03d}_{:03d}_{:03d}'.format(ih,iw,iz) )




class SimpleMerger():

	def _Run(self, parent, params, comm_title):
		#
		z_info = params['z_info']
		ext    = params['ext']

		i_slice_0 = z_info[0][0]["i_slice"]
		ih, iw, iz = 0, 0, 0
		file_panel = os.path.join( \
			obtain_seg_dir(params,ih,iw,iz), \
			'{:04d}.{}'.format(i_slice_0, ext) )
		image = m.read_image(file_panel, ext)
		
		im_dtype  = image.dtype
		im_shape  = image.shape
		
		im_size_h = params['im_size_h']
		im_size_w = params['im_size_w']
		im_size_z = params['im_size_z']
		
		cropped_hs = params['cropped_hs']
		cropped_ws = params['cropped_ws']
		cropped_zs = params['cropped_zs']
		num_h = params['num_h']
		num_w = params['num_w']
		num_z = params['num_z']

		split_size_h   = params['Split size (h)']
		split_size_w   = params['Split size (w)']
		split_size_z   = params['Split size (z)']

		overlap_size_h = params['Overlap size (h)']
		overlap_size_w = params['Overlap size (w)']
		overlap_size_z = params['Overlap size (z)']
		overlap_size_z_2 = overlap_size_z // 2


		if len(im_shape) == 3:
			merged_im_size = (im_size_h, im_size_w, im_shape[2])
		else:
			merged_im_size = (im_size_h, im_size_w)


		_create_folder_merge(params)


		assign_panel_hs, assign_merged_hs = m.assign_regions_for_merge(im_size_h, split_size_h, overlap_size_h)
		assign_panel_ws, assign_merged_ws = m.assign_regions_for_merge(im_size_w, split_size_w, overlap_size_w)


		if len(z_info) >= 2:
			z_info = [z_info[0][:-overlap_size_z_2]] + \
				[ z_sub[overlap_size_z_2:-overlap_size_z_2 ] for z_sub in z_info[1:-1] ] + \
				[ z_info[-1][overlap_size_z_2:] ]
		else:
			pass

		# return z_info
		print('cropped_ws ', cropped_ws)
		print('cropped_hs ', cropped_hs)

		if params['Reflect padding'] == True:
			 z_info[0] = z_info[0][overlap_size_z:]


		for iz in  range( num_z ):
			for z_sub_info in z_info[iz]:
				merged_image = np.zeros( merged_im_size, dtype=im_dtype )
				for iw, ih in product( range(num_w), range(num_h) ):
					file_panel = os.path.join( \
						obtain_seg_dir(params,ih,iw,iz), \
						'{:04d}.{}'.format(z_sub_info['i_slice'], ext) )
					cropped_image = m.read_image(file_panel, ext)
					#
					mh = assign_merged_hs[ih]
					ph = assign_panel_hs[ih]
					mw = assign_merged_ws[iw]
					pw = assign_panel_ws[iw]
					merged_image[mh[0]:mh[1], mw[0]:mw[1]] = cropped_image[ph[0]:ph[1], pw[0]:pw[1]]
				
				if params['Reflect padding'] == True:
					merged_image = merged_image[overlap_size_h:-overlap_size_h, overlap_size_w:-overlap_size_w]
				
				base_name = os.path.splitext(os.path.basename(z_sub_info['image_file']))[0]
				file_merged = os.path.join(params['Merged segmentation folder'], \
					'{}.{}'.format( base_name, ext ) )
				print('file_merged: ', file_merged)
				m.imwrite(file_merged, merged_image)

				#if params['Reflect padding'] == True:
				#	image = np.pad(image, pad_width=pad_width, mode='reflect')



		#
		print(comm_title, 'was finished.')
		return True

	def __init__(self, u_info):
		##
		self.u_info = u_info
		self.paramfile = os.path.join(u_info.parameters_path, "SimpleMerger.pickle")

		self.title = 'Splitter'

		self.tips = [
		                'Merged segmentation folder'
		                ]

		self.args = [
		                ['Merged segmentation folder (Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder']
		    ]


