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

import networkx as nx


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


def _connector(reference, target, threshold):

	TH = threshold / 100
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


class Connector():

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
		# Preprocessing
		self.split_folder = params['Split img/seg folder (Split)']
		self.threshold = int( params['Overlap level for connected components (%)'] )
		self.merge_folder   = params['Merged segmentation folder (Empty)']
		self.merge_filetype = params['Merged segmentation filetype']

		if (len(self.split_folder) == 0) or (len(self.merge_folder) == 0):
			print('Input/output folder unspecified.')
			return False


		
		filename = os.path.join(params['Split img/seg folder (Split)'], 'attr.json')
		with open(filename, 'r') as fp:
			p = json.load(fp)
		
		self.z_info       = p['z_info']
		self.reflect_pad  = p['Reflect padding']
		
		self.seg_folder   = p['Seg folder']
		
		self.ext          = p['ext']
		
		i_slice_0 = self.z_info[0][0]["i_slice"]
		ih, iw, iz = 0, 0, 0
		file_panel = os.path.join( \
			self.obtain_seg_dir(ih, iw, iz), \
			'{:04d}.{}'.format(i_slice_0, self.ext) )
		
		image = m.read_image(file_panel, self.ext)
		if image is None:
			print("Error: Split image was not loaded.")
			return False

		#self.im_dtype  = p['im_dtype']
		#self.im_shape  = p['im_shape']
		#
		
		#self.im_dtype  = image.dtype
		self.im_dtype  = np.int64
		self.im_shape  = image.shape
		
		self.im_size_h = int(p['im_size_h'])
		self.im_size_w = int(p['im_size_w'])
		self.im_size_z = int(p['im_size_z'])
		
		#cropped_hs = p['cropped_hs']
		#cropped_ws = p['cropped_ws']
		#cropped_zs = p['cropped_zs']
		self.num_h = int(p['num_h'])
		self.num_w = int(p['num_w'])
		self.num_z = int(p['num_z'])

		self.split_size_h   = int(p['Split size (h)'])
		self.split_size_w   = int(p['Split size (w)'])
		self.split_size_z   = int(p['Split size (z)'])

		self.overlap_size_h = int(p['Overlap size (h)'])
		self.overlap_size_w = int(p['Overlap size (w)'])
		self.overlap_size_z = int(p['Overlap size (z)'])
		print('overlap_size_z ', self.overlap_size_z)
		self.overlap_size_z_2 = self.overlap_size_z // 2

		#self.overlap_size_h_2 = self.overlap_size_h // 2
		#self.overlap_size_w_2 = self.overlap_size_w // 2

		
		# Slices per (ih, iw, iz)
		self.i_slices   = np.empty((self.num_h, self.num_w, self.num_z), dtype=object)
		for iz in  range( self.num_z ):
			for iw, ih in product( range( self.num_w ), range( self.num_h ) ):
				self.i_slices[ih,iw,iz]   = [ z_sub_info['i_slice'] for z_sub_info in self.z_info[iz] ]
		
		self.connector()
		self.merger()
		print(comm_title, 'was finished.')
		parent.parent.ExecuteCloseFileFolder(self.merge_folder)
		parent.parent.OpenFolder(self.merge_folder)
		
		return True
		
		
	def connector(self):
		
		
		# print('ids_unique ', ids_unique)
		
		# connector
		self.g = nx.Graph()
		
		print('connection in z')
		size_hh = (0, self.split_size_h)
		size_ww = (0, self.split_size_w)
		for ih, iw, iz in product( range(self.num_h), range(self.num_w), range(self.num_z-1) ):
			print('ih, iw, iz ', ih, iw, iz )
			### Connection z
			v_sub_ref  = self.load_seg_volume(ih, iw,   iz, size_hh, size_ww, [-self.overlap_size_z-1,-1])
			v_sub_targ = self.load_seg_volume(ih, iw, iz+1, size_hh, size_ww, [0,self.overlap_size_z])
			#print('v_sub_ref.shape  ', v_sub_ref.shape)
			#print('v_sub_targ.shape ', v_sub_targ.shape)
			ids_connector = _connector(v_sub_ref, v_sub_targ, self.threshold)
			self.g = register_graph(self.g, ids_connector, (ih, iw, iz), (ih, iw, iz+1))


		print('connection in h')
		size_hh_ref  = (self.split_size_h-self.overlap_size_h, self.split_size_h)
		size_hh_targ = (0, self.overlap_size_h)
		size_ww = (0, self.split_size_w)
		for ih, iw, iz in product( range(self.num_h-1), range(self.num_w), range(self.num_z) ):
			print('ih, iw, iz ', ih, iw, iz )
			### Reference volume
			v_sub_ref  = self.load_seg_volume(  ih, iw, iz, size_hh_ref , size_ww, [0,-1] )
			v_sub_targ = self.load_seg_volume(ih+1, iw, iz, size_hh_targ, size_ww, [0,-1] )
			ids_connector = _connector(v_sub_ref, v_sub_targ, self.threshold)
			self.g = register_graph(self.g, ids_connector, (ih, iw, iz), (ih+1, iw, iz))


		print('connection in w')
		size_hh = (0, self.split_size_h)
		size_ww_ref  = (self.split_size_w-self.overlap_size_w, self.split_size_w)
		size_ww_targ = (0, self.overlap_size_w)
		for ih, iw, iz in product( range(self.num_h), range(self.num_w-1), range(self.num_z) ):
			print('ih, iw, iz ', ih, iw, iz )
			### Reference volume
			v_sub_ref  = self.load_seg_volume(ih,   iw, iz, size_hh, size_ww_ref , [0,-1])
			v_sub_targ = self.load_seg_volume(ih, iw+1, iz, size_hh, size_ww_targ, [0,-1])
			ids_connector = _connector(v_sub_ref, v_sub_targ, self.threshold)
			self.g = register_graph(self.g, ids_connector, (ih, iw, iz), (ih, iw+1, iz))
		
		##
		## from graph 'g' to dict ids_unique
		##
		print('Check cross split-volume objects.')
		id_color = 1
		for subs in sorted(nx.connected_components(self.g), key=len, reverse=True):
			#print('id_color', id_color)
			for sub in subs:
				self.g.nodes[sub]['id_color'] = id_color
			id_color += 1
		
		print('Check split-volume specific objects.')
		self.ids_unique = np.empty((self.num_h, self.num_w, self.num_z), dtype=object)
		connected_id_list = list(self.g.nodes)
		for ih, iw, iz in product( range(self.num_h), range(self.num_w), range(self.num_z) ):
			seg_dir = self.obtain_seg_dir(ih, iw, iz)
			ids  = {}
			for id in load_unique_ids( seg_dir, self.i_slices[ih,iw,iz], self.ext, self.im_dtype ):
				node_name = '{:03d}_{:03d}_{:03d}_{:d}'.format(ih,iw,iz,id)
				if node_name not in connected_id_list:
					ids[id] = id_color
					id_color += 1
				else:
					ids[id] = self.g.nodes[node_name]['id_color']
			self.ids_unique[ih,iw,iz] = ids
		self.num_color = id_color
		print( 'self.num_color ', self.num_color )
		
		
	def merger(self):
		##
		##
		##
		merged_im_dtype = np.uint16
		merged_im_size  = (self.im_size_h, self.im_size_w)

		if  'color' in self.merge_filetype:
			colormap = np.random.randint(255, size=(self.num_color+1, 3), dtype=np.uint8)
			colormap[0,:] = 0
		else:
			colormap = None

		if  'TIFF' in self.merge_filetype:
			merged_ext = 'tif'
		elif 'PNG' in self.merge_filetype:
			merged_ext = 'png'
		else:
			print('Internal error about the output filetype.')
			exit()
		##
		##
		##
		assign_panel_hs, assign_merged_hs = m.assign_regions_for_merge(self.im_size_h, self.split_size_h, self.overlap_size_h)
		assign_panel_ws, assign_merged_ws = m.assign_regions_for_merge(self.im_size_w, self.split_size_w, self.overlap_size_w)
		z_info = self.z_info
		if len(z_info) >= 2:
			z_info = [z_info[0][:-self.overlap_size_z_2]] + \
				[ z_sub[self.overlap_size_z_2:-self.overlap_size_z_2 ] for z_sub in z_info[1:-1] ] + \
				[ z_info[-1][self.overlap_size_z_2:] ]
		else:
			pass
		if self.reflect_pad == True:
			 z_info[0] = z_info[0][self.overlap_size_z:]
		##
		##
		##
		for iz in  range(self.num_z ):
			for z_sub_info in z_info[iz]:
				#print('iz, ', iz)
				merged_image = np.zeros( merged_im_size, dtype = merged_im_dtype )
				for iw, ih in product( range( self.num_w ), range( self.num_h ) ):
					file_panel = os.path.join( self.obtain_seg_dir(ih,iw,iz), '{:04d}.{}'.format(z_sub_info['i_slice'], self.ext) )
					cropped_image = m.read_seg_image(file_panel, self.ext)
					mh = assign_merged_hs[ih]
					ph = assign_panel_hs[ih]
					mw = assign_merged_ws[iw]
					pw = assign_panel_ws[iw]
					tmp = cropped_image[ph[0]:ph[1], pw[0]:pw[1]]
					ids = self.ids_unique[ih,iw,iz]
					#print('ids ', ids)
					imgArray = np.zeros_like(tmp, dtype=merged_im_dtype)
					for i in range(tmp.shape[0]):
						for j in range(tmp.shape[1]):
							# print('tmp[i, j]' , tmp[i, j] )
							imgArray[i, j] = ids[tmp[i, j]]
					merged_image[mh[0]:mh[1], mw[0]:mw[1]] = imgArray
					
				if self.reflect_pad == True:
					merged_image = merged_image[self.overlap_size_h:-self.overlap_size_h, \
						self.overlap_size_w:-self.overlap_size_w]

				# print('np.unique(merged_image) ' , np.unique(merged_image, return_counts=True) )

				base_name = os.path.splitext(os.path.basename(z_sub_info['image_file']))[0]
				filename_merged = os.path.join( self.merge_folder, '{}.{}'.format( base_name, merged_ext ) )
				print('filename_merged: ', filename_merged)
				# m.imwrite(file_merged, merged_image)
				self.save_image(merged_image, filename_merged, self.merge_filetype, colormap = colormap)
		##
		##
		##
	
	def __init__(self, u_info):
		##
		self.u_info = u_info
		self.paramfile = os.path.join(u_info.parameters_path, "SimpleMerger.pickle")

		self.title = 'Splitter'

		self.tips = [
		                'Split img/seg folder (Split)',
		                'Threshold for connected components',
		                'Merged segmentation folder',
                        'Output filetype'
		                ]

		self.args = [
		                ['Split img/seg folder (Split)',  'SelectSplitterFolder', 'OpenSplitterFolder'],
		                ['Overlap level for connected components (%)', 'SpinBox', [0, 80, 100]],
		                ['Merged segmentation folder (Empty)',  'SelectEmptyFolder', 'OpenEmptyFolder'],
                        ['Merged segmentation filetype', 'ComboBox', ["8-bit color PNG", "16-bit gray scale PNG", "8-bit gray scale PNG", "8-bit color TIFF", "16-bit gray scale TIFF", "8-bit gray scale TIFF"]]
		    		]


