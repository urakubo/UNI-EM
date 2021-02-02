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
import cv2


main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
#sys.path.append(path.join(main_dir, "system"))
import miscellaneous.Miscellaneous as m


class ImagesExe():

	def _Run(self, parent, params, comm_title):
		##
		targ = parent.SharedPreprocess(params, comm_title)
		##
		file_exts  = [ "*.tif", "*.tiff", "*.png", "*.PNG" ]
		seg_files = []
		for ext in file_exts:
			seg_files.extend( glob.glob(os.path.join(params['Segmentation image folder'], ext) ))
		if len(seg_files) == 0:
		    print('No tiff/png segmentation file.')
		    return False
		seg_files = sorted(seg_files)

		sg = m.imread(seg_files[0], cv2.IMREAD_GRAYSCALE)
		print('')
		print('Number of segmentation images : ', len(seg_files))
		print('Segmentation image dimensions : ', sg.shape)
		print('Segmentation datatype         : ', sg.dtype)
		print('')

		ch = int(params['Downsampling factor in X'])
		cw = int(params['Downsampling factor in Y'])
		cz = int(params['Downsampling factor in Z'])
		xysize = sg[::cw,::ch].shape
		seg_files = seg_files[::cz]
		ids_volume = np.zeros((xysize[0], xysize[1], len(seg_files)), dtype=sg.dtype)

		for i, seg_file in enumerate(seg_files):
			seg = m.imread(seg_file, cv2.IMREAD_GRAYSCALE)
			ids_volume[:,:,i] = seg[::cw,::ch]

		parent.SharedGenerateInfoFile(ids_volume, targ.surfaces_segment_info_json_file)
		return parent.SharedPostProcess(params, targ, ids_volume)


