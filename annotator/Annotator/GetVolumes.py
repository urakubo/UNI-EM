
import os, sys
from os import path
import trimesh
import pymeshfix
import gzip
import pickle
import numpy as np
import glob


def GetVolumes(surface_path, paint_path):

	whole_mesh_names = glob.glob(os.path.join(surface_path, "*.stl"))
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
			data['volume'] = None
			with open(part_mesh_name, 'wb') as file:
				pickle.dump(data, file)
			print('Delete volume: ', part_mesh_name)
			continue
			"""

			if ('volume' in data) and (data['volume'] != None): # 左の結果が偽の場合は、右の処理は実行されない。
				print('Volume already exists: ', part_mesh_name)
				continue
			else :
				volume = GetOneVolume(v,f,data['painted'])
				if volume is not None :
					data['volume'] = volume
					print('Volume of ' + part_mesh_name + ' : ', data['volume'])
					with open(part_mesh_name, 'wb') as file:
						pickle.dump(data, file)


def GetOneVolume(v,f,data):

	unzipped_tri = gzip.decompress(data)
	sub_face_id = []
	for i in range( f.shape[0] ) :
		if (unzipped_tri[i*3:i*3+3] == b'\x01\x01\x01') :
			sub_face_id.append(f[i,:])

	part_mesh = pymeshfix.MeshFix(v, np.array(sub_face_id))
	part_mesh.repair()
	# part_mesh.plot() # Visualization of cloased meshes

	closed_v = part_mesh.v # numpy np.float array
	closed_f = part_mesh.f # numpy np.int32 array

	closed_mesh = trimesh.Trimesh(vertices=closed_v, faces=closed_f)
	# print("Volume: ", closed_mesh.volume) # Numpy-stl (mesh) にも同ルーチン有

	return closed_mesh.volume



