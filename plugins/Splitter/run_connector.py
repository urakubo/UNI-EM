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


def load_unique_ids( folder, i_slices, ext, im_dtype ):

	ids_unique = []
	for i, i_slice in enumerate(i_slices):
		file_panel    = os.path.join(folder, '{:04d}.{}'.format(i_slice, ext) )
		image         = m.read_seg_image(file_panel, ext)
		ids_unique.append( np.unique(image) )
	ids_unique = np.unique( np.hstack(ids_unique) )
	return ids_unique


def load_volume( folder, i_slices, ext, im_dtype, size_hh, size_ww ):

	volume = np.zeros( [size_hh[1]-size_hh[0], size_ww[1]-size_ww[0], len(i_slices)], dtype=im_dtype )
	for i, i_slice in enumerate(i_slices):
		file_panel    = os.path.join(folder, '{:04d}.{}'.format(i_slice, ext) )
		image         = m.read_seg_image(file_panel, ext)
		volume[:,:,i] = image[size_hh[0]:size_hh[1], size_ww[0]:size_ww[1]]
	return volume


def connector(reference, target):

	TH = 0.8
	connection = []
	for id_ref, count_ref in zip( *np.unique(reference, return_counts=True) ) :
		t = target[reference == id_ref]
		ids, counts = np.unique( t, return_counts=True )
		ids = ids[ counts/count_ref > TH ]
		connection.extend([(id_ref, id) for id in ids])
	# print('connection ref->targ ', connection)

	for id_targ, count_targ in zip( *np.unique( target, return_counts=True) ) :
		t = reference[target == id_targ]
		ids, counts = np.unique( t, return_counts=True )
		ids = ids[ counts/count_targ > TH ]
		connection.extend([(id, id_targ) for id in ids])

	connection = list(set(connection))
	return connection


def register_graph( g, ids_connector, ref_hwz, targ_hwz ):

	ref_ih = ref_hwz[0]
	ref_iw = ref_hwz[1]
	ref_iz = ref_hwz[2]
	targ_ih = targ_hwz[0]
	targ_iw = targ_hwz[1]
	targ_iz = targ_hwz[2]
	
	for ref_targ in ids_connector:
		ref  = '{:03d}_{:03d}_{:03d}_{:d}'.format(ref_ih, ref_iw, ref_iz, ref_targ[0]) 
		g.add_node(ref, \
			ih = ref_ih, \
			iw = ref_iw, \
			iz = ref_iz, \
			id  = ref_targ[0])
		targ = '{:03d}_{:03d}_{:03d}_{:d}'.format(targ_ih, targ_iw, targ_iz, ref_targ[1]) 
		g.add_node(targ, \
			ih = targ_ih, \
			iw = targ_iw, \
			iz = targ_iz, \
			id  = ref_targ[1])
		g.add_edge(ref, targ)

	return g


class SimpleMerger():

	def save_image(self, image2d, filename, filetype, colormap = None):
		if filetype == '16-bit gray scale TIFF':
			m.save_tif16(image2d, filename)
		elif filetype == '8-bit gray scale TIFF':
			m.save_tif8(image2d, filename)
		elif filetype == '16-bit gray scale PNG':
			m.save_png16(image2d, filename)
		elif filetype == '8-bit gray scale PNG':
			m.save_png8(image2d, filename)
		elif filetype == '8-bit color PNG' :
			m.save_pngc(image2d, filename, colormap)
		elif filetype == '8-bit color TIFF' :
			m.save_tifc(image2d, filename, colormap)
		else:
			print('Segmentation was not saved.')

	
	def load_seg_volume(self, ih, iw, iz, size_hh, size_ww, size_zz):
		seg_dir = os.path.join(self.split_folder, self.seg_folder, '{:03d}_{:03d}_{:03d}'.format(ih,iw,iz) )
		return load_volume( seg_dir, \
			self.i_slices[ih, iw, iz][size_zz[0]:size_zz[1]], \
			self.ext, self.im_dtype, size_hh, size_ww )
	
	
	def obtain_seg_dir(self, ih, iw, iz):
		return os.path.join(self.split_folder, self.seg_folder, '{:03d}_{:03d}_{:03d}'.format(ih,iw,iz) )
	
	
	
	def _Run(self, parent, params, comm_title):
		#
		self.merge_folder   = params['Merged segmentation folder']
		self.merge_filetype = params['Merged segmentation filetype']
		self.z_info       = params['z_info']
		self.reflect_pad  = params['Reflect padding']
	
		self.split_folder = params['Split img/seg folder']
		self.seg_folder   = params['Seg folder']
	
		self.ext       = params['ext']
		self.im_dtype  = params['im_dtype']
		self.im_dtype  = np.int64
		
		self.im_shape  = params['im_shape']
		
		
		self.im_size_h = params['im_size_h']
		self.im_size_w = params['im_size_w']
		self.im_size_z = params['im_size_z']
		
		self.cropped_hs = params['cropped_hs']
		self.cropped_ws = params['cropped_ws']
		self.cropped_zs = params['cropped_zs']
		self.num_h = params['num_h']
		self.num_w = params['num_w']
		self.num_z = params['num_z']

		self.split_size_h   = params['Split size (h)']
		self.split_size_w   = params['Split size (w)']
		self.split_size_z   = params['Split size (z)']

		self.overlap_size_h = params['Overlap size (h)']
		self.overlap_size_w = params['Overlap size (w)']
		self.overlap_size_z = params['Overlap size (z)']
		self.overlap_size_h_2 = self.overlap_size_h // 2
		self.overlap_size_w_2 = self.overlap_size_w // 2
		self.overlap_size_z_2 = self.overlap_size_z // 2

		
		# Slices per (ih, iw, iz)
		self.i_slices   = np.empty((self.num_h, self.num_w, self.num_z), dtype=object)
		for iz in  range( self.num_z ):
			for iw, ih in product( range( self.num_w ), range( self.num_h ) ):
				self.i_slices[ih,iw,iz]   = [ z_sub_info['i_slice'] for z_sub_info in self.z_info[iz] ]
		
		self.connector()
		self.merger()
		print(comm_title, 'was finished.')
		return True
		
		
		
	
	
	def __init__(self, u_info):
		##
		self.u_info = u_info
		self.paramfile = os.path.join(u_info.parameters_path, "SimpleMerger.pickle")

		self.title = 'Splitter'

		self.tips = [
		                'Merged segmentation folder',
                        'Output filetype'
		                ]

		self.args = [
		                ['Merged segmentation folder (Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder'],
                        ['Merged segmentation Filetype', 'ComboBox', ["8-bit color PNG", "16-bit gray scale PNG", "8-bit gray scale PNG", 
                                                         "8-bit color TIFF", "16-bit gray scale TIFF", "8-bit gray scale TIFF"]]
		    ]


