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
			print('Container must be integers, but ', ids_volume.dtype)
			return False

		ch = int(params['Downsampling factor in X'])
		cw = int(params['Downsampling factor in Y'])
		cz = int(params['Downsampling factor in Z'])
		ids_volume = ids_volume[::cw,::ch,::cz]

		parent.SharedGenerateInfoFile(ids_volume, targ.surfaces_segment_info_json_file)
		return parent.SharedPostProcess(params, targ, ids_volume)


