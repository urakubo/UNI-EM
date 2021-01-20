
import os, sys, time
from os import path
import trimesh
import pymeshfix
import gzip
import pickle
import numpy as np
import glob
import h5py


def GetVolumes(surface_path, paint_path, skeleton_path):

	whole_mesh_filenames = glob.glob(os.path.join(surface_path, "*.stl"))
	ids_volumes  = {}
	for whole_mesh_filename in whole_mesh_filenames :
		whole_mesh_name_wo_ext  = os.path.splitext(os.path.basename(whole_mesh_filename))[0]
		part_mesh_name_wildcard = os.path.normpath(os.path.join(paint_path, whole_mesh_name_wo_ext+"-*.pickle"))
		part_mesh_filenames = glob.glob(part_mesh_name_wildcard)

		## Check whether painted meshes
		if part_mesh_filenames == [] :
			continue

		## Load surface meshes
		whole_mesh = trimesh.load( whole_mesh_filename )
		surf_vertices = whole_mesh.vertices
		surf_faces    = whole_mesh.faces

		## Load skeletons
		skel = {}
		skeleton_filename = os.path.normpath(os.path.join(skeleton_path, whole_mesh_name_wo_ext+".hdf5"))
		if os.path.isfile( skeleton_filename ) :
			with h5py.File( skeleton_filename ,'r') as f:
				skel['vertices'] = f['vertices'][()]
				skel['radiuses'] = f['radiuses'][()]
				if 'lengths' in f.keys() :
					skel['lengths']  = f['lengths'][()]

		for part_mesh_filename in part_mesh_filenames :
			with open(part_mesh_filename, 'rb') as file:
				data = pickle.load(file)

			"""
			if ('volume' in data) and (data['volume'] != None): # 左の結果が偽の場合は、右の処理は実行されない。
				print('Volume already exists: ', part_mesh_name)
				continue
			"""
			closed_mesh = GetVolume(surf_vertices, surf_faces, data['painted'])
			if closed_mesh.volume is not None :
				# print('Volume of ' + part_mesh_name + ' : ', volume)
				id = os.path.basename(part_mesh_filename) 
				id = os.path.splitext(id)[0]
				id = int( id.split('-')[1] )
				print('ID: ', id,', Volume:', closed_mesh.volume)
				if id in ids_volumes:
					ids_volumes[id] += closed_mesh.volume
				else:
					ids_volumes[id] = closed_mesh.volume

			if skel != {}:
				radiuses, length = GetRadiusLength(closed_mesh, skel)


		return ids_volumes

"""
	if ids_volumes is not {} :
		counter = s.update_paint_volumes(ids_volumes)

		counter = s.update_paint_volumes(ids_volumes)
		loop = asyncio.get_event_loop()
		result = loop.run_until_complete(counter)
		loop.close()
"""

def GetVolume(v,f,data):

	unzipped_tri = gzip.decompress(data)
	sub_face_id = []
	for i in range( f.shape[0] ) :
		if (unzipped_tri[i*3:i*3+3] == b'\x01\x01\x01') :
			sub_face_id.append(f[i,:])

	part_mesh = pymeshfix.MeshFix(v, np.array(sub_face_id))
	part_mesh.repair()
	part_mesh.plot() # Visualization of cloased meshes

	closed_v = part_mesh.v # numpy np.float array
	closed_f = part_mesh.f # numpy np.int32 array

	closed_mesh = trimesh.Trimesh(vertices=closed_v, faces=closed_f)
	# print("Volume: ", closed_mesh.volume)
	# Numpy-stl (mesh) にも同ルーチン有
	return closed_mesh


def GetRadiusLength(closed_mesh, skel):

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

