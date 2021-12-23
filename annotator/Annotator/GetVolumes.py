
import os, sys, time
from os import path
import trimesh
import pymeshfix
import gzip
import pickle
import numpy as np
import glob
import h5py
import pyvista as pv

class GetVolumes:

	def __init__( self, surface_path, paint_path, skeleton_path):
		self.surface_path  = surface_path
		self.paint_path    = paint_path
		self.skeleton_path = skeleton_path

	def exec(self):
		attributes  = {}
		for whole_mesh_filename in glob.glob(os.path.join(self.surface_path, "*.stl")) :

			# Check whether painted files exist or not.
			whole_mesh_name_wo_ext  = os.path.splitext(os.path.basename(whole_mesh_filename))[0]
			part_mesh_name_wildcard = os.path.normpath(os.path.join(self.paint_path, whole_mesh_name_wo_ext+"-*.pickle"))
			part_mesh_filenames = glob.glob(part_mesh_name_wildcard)
			if part_mesh_filenames == [] :
				continue

			# Load surface meshes
			whole_mesh = trimesh.load( whole_mesh_filename )
			surf_vertices = whole_mesh.vertices
			surf_faces    = whole_mesh.faces

			# Load skeletons
			skel = {}
			skeleton_filename = os.path.normpath(os.path.join(self.skeleton_path, whole_mesh_name_wo_ext+".hdf5"))
			if os.path.isfile( skeleton_filename ) :
				with h5py.File( skeleton_filename ,'r') as f:
					skel['vertices'] = f['vertices'][()]
					skel['radiuses'] = f['radiuses'][()]
					if 'lengths' in f.keys() :
						skel['lengths']  = f['lengths'][()]

			for part_mesh_filename in part_mesh_filenames :
				with open(part_mesh_filename, 'rb') as file:
					data = pickle.load(file)

				closed_mesh, closed_mesh_for_vtk, area = self._get_volume(surf_vertices, surf_faces, data['painted'])
				if closed_mesh.volume is None :
					continue
				id = os.path.splitext(os.path.basename(part_mesh_filename))[0]
				id = int( id.split('-')[1] )

				# print('Surface ID          : ', whole_mesh_name_wo_ext)
				# print('Paint   ID          : ', id)
				# print('Painted area (um2)  : ', area)
				# print('Volume (um3)        : ', closed_mesh.volume)
				text_vtk = "Surface ID : {0}\nPaint ID: {1}\nPainted area (um2): {2:.4f}\nVolume (um3): {3:.4f}\n".format(whole_mesh_name_wo_ext, id, area, closed_mesh.volume)

				# Keep values
				if id in attributes.keys():
					attributes[id]['volume'] += closed_mesh.volume
					attributes[id]['area']   += area
				else:
					attributes[id] = {}
					attributes[id]['volume']      = closed_mesh.volume
					attributes[id]['area']        = area
					attributes[id]['length']      = 0
					attributes[id]['min_radius']  = 0
					attributes[id]['max_radius']  = 0
					attributes[id]['mean_radius'] = 0

				# If skeleton exists:
				if skel != {}:
					len_enclosed, len_tot, min_radius, max_radius, mean_radius = self._get_radius_length(closed_mesh, skel)
					# print('Total length (um)   : ', len_tot )
					# print('Enclosed length (um): ', len_enclosed )
					# print('Minimum radius (um) : ', min_radius )
					# print('Maximum radius (um) : ', max_radius )
					# print('Mean radius (um)    : ', mean_radius )
					text_vtk2 = "Length (um) : {0:.4f}\nMin r (um) : {1:.4f}\nMax r (um) : {2:.4f}\nMean r (um) : {3:.4f}".format(len_enclosed, min_radius, max_radius, mean_radius)
					text_vtk = text_vtk + text_vtk2

					# Save values
					attributes[id]['length']      += len_enclosed
					attributes[id]['max_radius']  = max( [ attributes[id]['max_radius'], max_radius ] )
					attributes[id]['mean_radius'] = mean_radius
					if attributes[id]['min_radius'] <= 0:
						attributes[id]['min_radius']  = min_radius
					else:
						attributes[id]['min_radius']  = min( [ attributes[id]['min_radius'], min_radius ] )

				plotter = pv.Plotter()
				plotter.add_mesh(closed_mesh_for_vtk, label='mesh')
				plotter.add_text(text_vtk)
				plotter.show()

			return attributes

	"""
	if ids_volumes is not {} :
		counter = s.update_paint_volumes(ids_volumes)

		counter = s.update_paint_volumes(ids_volumes)
		loop = asyncio.get_event_loop()
		result = loop.run_until_complete(counter)
		loop.close()
	"""

	def _get_volume(self, v, f, data):
		unzipped_tri = gzip.decompress(data)
		sub_face_id = []
		for i in range( f.shape[0] ) :
			if (unzipped_tri[i*3:i*3+3] == b'\x01\x01\x01') :
				sub_face_id.append(f[i,:])

		mesh = trimesh.Trimesh(v, np.array(sub_face_id))
		mesh.merge_vertices()
		mesh.remove_degenerate_faces()
		mesh.remove_duplicate_faces()
		vclean = mesh.vertices
		fclean = mesh.faces

	#	vclean, fclean = pymeshfix.clean_from_arrays(v, np.array(sub_face_id))
		part_mesh = pymeshfix.MeshFix(vclean, fclean)

		area = part_mesh.mesh.area
		part_mesh.repair()

		closed_v = part_mesh.v # numpy np.float array
		closed_f = part_mesh.f # numpy np.int32 array

		closed_mesh = trimesh.Trimesh(vertices=closed_v, faces=closed_f)
		# print("Volume: ", closed_mesh.volume)
		# Numpy-stl (mesh) にも同ルーチン有
		return closed_mesh, part_mesh.mesh, area

	def _get_radius_length(self, closed_mesh, skel):

		closed_vertices = np.array( closed_mesh.vertices )
		closed_faces    = np.array( closed_mesh.faces )
		num = closed_faces.shape[0]
		closed_faces = np.hstack([np.ones([num,1]).astype(int)*3,closed_faces])
		closed_mesh_pv  = pv.PolyData(np.array(closed_vertices), np.array(closed_faces))

		ugrid = pv.UnstructuredGrid()
		ugrid.points = skel['vertices']

		selection = ugrid.select_enclosed_points(closed_mesh_pv, tolerance=0.0, check_surface=False)
		mask = selection.point_arrays['SelectedPoints'].view(np.bool)

		len_tot       = np.sum(skel['lengths'][:])

		if np.any(mask) :
			len_enclosed  = np.sum(skel['lengths'][mask == True])
			radius_min    = np.min(skel['radiuses'][mask == True])
			radius_max    = np.max(skel['radiuses'][mask == True])
			radius_mean   = np.dot(skel['lengths'][mask == True], skel['radiuses'][mask == True]) / len_enclosed

		else :
			len_enclosed  = 0
			radius_min    = 0
			radius_max    = 0
			radius_mean   = 0

		return len_enclosed, len_tot, radius_min, radius_max, radius_mean


	def _get_radius_length_old(closed_mesh, skel):

		print('Calculating distances ... ')

		obj = trimesh.proximity.ProximityQuery(closed_mesh)
		dists = obj.signed_distance(skel['vertices'])
		# print('skel["vertices"]: ', skel['vertices'])
		# print('Signed distance : ', dists)

		print('Number of positive distances: ', np.sum(dists >  0))
		print('Number of negative distances: ', np.sum(dists <= 0))

		tot_len1 = np.sum(skel['lengths'][dists>0])
		tot_len2 = np.sum(skel['lengths'][dists<=0])

		print('Total length of positives: ', tot_len1 )
		print('Total length of negatives: ', tot_len2 )

		return tot_len1, tot_len2

	#	if 'lengths' in f.keys() :
	#		skel['lengths']  = f['lengths'][()]

