###
###
###
import sys, os, time, errno
from os import path, pardir
import glob
import numpy as np
import json
import sqlite3
import h5py



main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
#sys.path.append(path.join(main_dir, "system"))
import miscellaneous.Miscellaneous as m


class Hdf5Exe():

	def _Run(self, parent, params, comm_title):

		##
		targ = parent.SharedPreprocess(params, comm_title)
		##
		with h5py.File(params['Hdf5 file containing segmentation volume'], 'r') as f:
			if params['Container name'] not in f.keys():
				print('No container: ', params['Container name'])
				return False
			ids_volume = f[ params['Container name'] ][()]

		if ids_volume.ndim != 3 :
			print('Container must be 3D, but ', ids_volume.ndime)
			return False

		if ids_volume.dtype not in ['int8','int16','int32','int64','uint8','uint16','uint64']:
			print('Container must have integers, but ', ids_volume.dtype)
			return False

		ids_nums = np.unique(ids_volume, return_counts=True)
		ids   = ids_nums[0]
		names = [str(id).zfill(10) for id in ids]
		sizes = ids_nums[1]
		colormap = np.random.randint(255, size=(ids.shape[0], 3), dtype='int')

		if ids[0] == 0:
			ids   = np.delete(ids, 0)
			names.pop(0)
			sizes = np.delete(sizes, 0)
			colormap = np.delete(colormap, 0, 0)

		ids      = ids.tolist()
		sizes    = sizes.tolist()
		colormap = colormap.tolist()

		print('Constainer shape: ', ids_volume.shape)
		print('IDs  : ', ids)
		print('names: ', names)
		print('sizes: ', sizes)
		print('colos: ', colormap)

		##
		keys = ['id', 'name', 'size']
		data_dict = [dict(zip(keys, valuerecord)) for valuerecord in zip(ids, names, sizes)]

		for i in range(len(data_dict)):
			col = {'confidence': 0, 'r': colormap[i][0], 'g': colormap[i][1],  'b': colormap[i][2],  'act': 0}
			data_dict[i].update(col)

		print('data_dict: ', data_dict)

		with open( targ.surfaces_segment_info_json_file , 'w') as f:
			json.dump(data_dict, f, indent=2, ensure_ascii=False)

		## Postprocess
		return parent.SharedPostProcess(params, targ, ids_volume)


