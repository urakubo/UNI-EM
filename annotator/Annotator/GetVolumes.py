
import os, sys, time
from os import path
import trimesh
import pymeshfix
import gzip
import pickle
import numpy as np
import glob


def GetVolumes(surface_path, paint_path):

	whole_mesh_names = glob.glob(os.path.join(surface_path, "*.stl"))
	ids_volumes  = {}
	for whole_mesh_name in whole_mesh_names :
		whole_mesh_name_wo_ext  = os.path.splitext(os.path.basename(whole_mesh_name))[0]
		part_mesh_name_wildcard = os.path.normpath(os.path.join(paint_path, whole_mesh_name_wo_ext+"-*.pickle"))
		part_mesh_names = glob.glob(part_mesh_name_wildcard)

		if part_mesh_names == [] :
			continue

		whole_mesh = trimesh.load( whole_mesh_name )
		v = whole_mesh.vertices
		f = whole_mesh.faces

		for part_mesh_name in part_mesh_names :
			with open(part_mesh_name, 'rb') as file:
				data = pickle.load(file)

			"""
			if ('volume' in data) and (data['volume'] != None): # 左の結果が偽の場合は、右の処理は実行されない。
				print('Volume already exists: ', part_mesh_name)
				continue
			"""

			volume = GetOneVolume(v,f,data['painted'])
			if volume is not None :
				# print('Volume of ' + part_mesh_name + ' : ', volume)
				id = os.path.basename(part_mesh_name) 
				id = os.path.splitext(id)[0]
				id = int( id.split('-')[1] )
				print('ID: ', id,', Volume:', volume)
				if id in ids_volumes:
					ids_volumes[id] += volume
				else:
					ids_volumes[id] = volume

		return ids_volumes

"""
	if ids_volumes is not {} :
		counter = s.update_paint_volumes(ids_volumes)

		counter = s.update_paint_volumes(ids_volumes)
		loop = asyncio.get_event_loop()
		result = loop.run_until_complete(counter)
		loop.close()
"""

def GetOneVolume(v,f,data):

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

	return closed_mesh.volume



