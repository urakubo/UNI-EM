##
##
import sys, os
import subprocess as s
from PyQt5.QtCore import Qt
import miscellaneous.Miscellaneous as m

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
# exec_template = ['python', os.path.join(main_dir, 'plugins', 'Template', 'run_example.py')]


import plugins.Multicut.elf_segmentation_multicut_part as mc
import plugins.Multicut.elf_segmentation_features_part as feats
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.filters import gaussian
import cv2
import numpy as np


class Multicut():
	def _Run(self, parent, params, comm_title):
        ##
        # try:
        ##
		print('')
		print(comm_title, 'is running..')
		print('')
		# Preprocessing
		inter_output_path = params['Intermediate output folder (2D Watershed, Empty)']
		final_output_path = params['Output segmentation folder (Empty)']
		if (len(inter_output_path) == 0) or (len(final_output_path) == 0):
		    print('Output folder unspecified.')
		    return False


		# Load membrane probability
		training_image_files = m.ObtainImageFiles(params['Membrane probability'])
		if len(training_image_files) == 0:
		    print('No membrane probability images.')
		    return False
		pmap = [m.imread(file, cv2.IMREAD_GRAYSCALE) for file in training_image_files]
		pmap = np.array(pmap)
		pmap = pmap.transpose((1,2,0))

		binary_image = np.logical_not(pmap > int(params['Binarization threshold']))
		watersheded   = np.zeros_like(pmap, dtype='int32')
		pmap = pmap.astype('float32')
		pmap = pmap / np.max(pmap)

		print('Process 1: watershed..')
		offset = 0
		for iz in range(watersheded.shape[2]):
			bi = binary_image[:,:,iz]
			distance = ndi.distance_transform_edt(bi)
			distance = gaussian(distance, sigma=float(params['Sigma for Gaussian smoothing']))

			local_maxi = peak_local_max(distance, labels=bi, min_distance=int(params['Minimal distance']) )
			mask = np.zeros(distance.shape, dtype=bool)
			mask[tuple(local_maxi.T)] = True
			markers, max_id = ndi.label(mask)

			wsz = watershed(-distance, markers, mask=None)
			wsz = wsz.astype('int32')
			wsz += offset
			offset += max_id
			watersheded[:,:,iz] = wsz

		print('Process 2: compute a region adjacency graph..')
		rag = feats.compute_rag(watersheded)

		print('Process 3: compute edge costs..')
		costs = feats.compute_boundary_features(rag, pmap)[:, 0]
		# We weight the costs by the size of the corresponding edge
		# for z and xy edges
		z_edges = feats.compute_z_edge_mask(rag, watersheded)
		xy_edges = np.logical_not(z_edges)
		edge_populations = [z_edges, xy_edges]
		edge_sizes = feats.compute_boundary_mean_and_length(rag, pmap)[:, 1]
		costs = mc.transform_probabilities_to_costs(costs, edge_sizes=edge_sizes, edge_populations=edge_populations)

		# run the multicut partitioning, here, we use the kernighan lin 
		# heuristics to solve the problem, introduced in
		# http://xilinx.asia/_hdl/4/eda.ee.ucla.edu/EE201A-04Spring/kl.pdf

		# ["kernighan lin", "greedy additive", "decomposition", "fusion moves", "greedy fixation"]

		print('Process 4: multicut partitioning, ', params['Multicut solver'],' ..' )
		trans_name = {'kernighan lin': 'kernighan-lin', \
			'greedy additive': 'greedy-additive', \
			'decomposition':'decomposition', \
			'fusion moves': 'fusion-moves', \
			'greedy fixation': 'greedy-fixation'}
		arg = {'name': trans_name[params['Multicut solver']], 'graph': rag, 'costs': costs}
		# node_labels = mc.get_multicut_solver(**arg )

		if params['Multicut solver'] == 'kernighan lin':
			node_labels = mc.multicut_kernighan_lin(rag, costs)
		elif params['Multicut solver'] == 'greedy additive':
			node_labels = mc.multicut_gaec(rag, costs)
		elif params['Multicut solver'] == 'decomposition':
			node_labels = mc.multicut_decomposition(rag, costs)
		elif params['Multicut solver'] == 'fusion moves':
			node_labels = mc.multicut_fusion_moves(rag, costs)
		else :
			print('Internal error occurs: ', params['Multicut solver'])
			return False


		segmentation = feats.project_node_labels_to_pixels(rag, node_labels)

		watersheded  = watersheded.astype('uint16')
		segmentation = segmentation.astype('uint16')

		# Save images 
		print('Process 5: Save images..')

		volume = segmentation
		filetype = params['Output filetype']
		folder   = params['Output segmentation folder (Empty)']
		flag = self._save_images(filetype, folder, volume, parent)

		volume = watersheded
		folder   = params['Intermediate output folder (2D Watershed, Empty)']
		filetype = params['Intermediate output filetype']
		flag = self._save_images(filetype, folder, volume, parent)


		print(comm_title, 'was finished.')
		#except:
        #    print("Error: h5 files (ground truth) were not generated.")
        #    return False


	def _save_images(self, filetype, folder, volume, parent):

		if (filetype == '8-bit color PNG') or (filetype == '8-bit color TIFF'):
			ids = np.max(volume)
			print('Max segmentation ID: ', ids)
			colormap = np.random.randint(255, size=(ids+2, 3), dtype=np.uint64)
			colormap[0,:] = 0

		m.UnlockFolder(parent.u_info, folder)
		for idz in range(volume.shape[2]):
		    image2d = volume[:, :, idz]
		    print('{} / {}'.format(idz, volume.shape[2]) )

		    if filetype == '16-bit gray scale TIFF':
		        filename = os.path.join(folder, 'z{:0=4}.tif'.format(idz))
		        m.save_tif16(image2d, filename)
		    elif filetype == '16-bit gray scale PNG':
		        filename = os.path.join(folder, 'z{:0=4}.png'.format(idz))
		        m.save_png16(image2d, filename)
		    elif filetype == '8-bit color PNG' :
		        filename = os.path.join(folder, 'z{:0=4}.png'.format(idz))
		        m.save_pngc(image2d, filename, colormap)
		    elif filetype == '8-bit color TIFF' :
		        filename = os.path.join(folder, 'z{:0=4}.tif'.format(idz))
		        m.save_tifc(image2d, filename, colormap)
		    else:
		        print('Data was not saved.')
		        return False
		parent.parent.ExecuteCloseFileFolder(folder)
		parent.parent.OpenFolder(folder)
		return True


	def __init__(self, u_info):
		##
		self.u_info = u_info

		self.paramfile = os.path.join(u_info.parameters_path, "Multicut.pickle")

		self.title = 'Multicut'

		self.tips = [
		                'Membrane probability',
		                'Multicut solver'
		                'Binarization threshold for boundary',
		                'Sigma for Gaussian smoothing',
		                'Minimal distance between seeds',
		                'Intermediate output folder',
		                'Intermediate output filetype',
		                'Output segmentation folder',
		                'Output filetype'
		                ]

		self.args = [
		                ['Membrane probability', 'SelectImageFolder', 'OpenImageFolder'],
		                ['Multicut solver', 'ComboBox', ["kernighan lin", "greedy additive", "decomposition", "fusion moves"]],
		                ['Binarization threshold', 'SpinBox', [1, 128, 255]],
		                ['Sigma for Gaussian smoothing', 'SpinBox', [0, 2, 255]],
		                ['Minimal distance', 'SpinBox', [0, 10, 255]],
		                ['Intermediate output folder (2D Watershed, Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder'],
		                ['Intermediate output filetype', 'ComboBox', ["8-bit color PNG", "8-bit color TIFF", "16-bit gray scale PNG","16-bit gray scale TIFF"]],
		                ['Output segmentation folder (Empty)',  'SelectEmptyModelFolder', 'OpenEmptyModelFolder'],
		                ['Output filetype', 'ComboBox', ["8-bit color PNG", "8-bit color TIFF", "16-bit gray scale PNG","16-bit gray scale TIFF"]],

		    ]

