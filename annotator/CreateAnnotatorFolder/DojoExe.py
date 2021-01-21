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
sys.path.append(path.join(main_dir, "system"))
from system.Params import Params
import miscellaneous.Miscellaneous as m


class DojoExe():

	def _Run(self, parent, params, comm_title):

		print(comm_title,' is running ...')
		ref = Params()
		ref.SetUserInfo(params['Dojo Folder'])
		targ = Params()
		targ.SetUserInfoAnnotator(params['Empty Folder for Annotator'])

		##
		print('Making directories.')
		##
		if os.path.isdir(targ.surfaces_path) == False:
			m.mkdir_safe(targ.surfaces_path)
			m.mkdir_safe(targ.surfaces_whole_path)
		if os.path.isdir(targ.skeletons_path) == False:
			m.mkdir_safe(targ.skeletons_path)
			m.mkdir_safe(targ.skeletons_whole_path)
		if os.path.isdir(targ.volume_path) == False:
			m.mkdir_safe(targ.volume_path)
		if os.path.isdir(targ.paint_path) == False:
			m.mkdir_safe(targ.paint_path)

		##
		print('Create database json file.')
		##

		## Load color file
		colordata = m.load_hdf5(ref.color_map_file, ref.hdf_color_name) 
		colnum = colordata.shape[0];

		## Load database file
		query = "select * from segmentInfo;"
		con = sqlite3.connect(  ref.segment_info_db_file )
		cur = con.cursor()
		cur.execute( query ) # Obtain max id
		data = cur.fetchall()
		con.close()

		keys = ['id', 'name', 'size', 'confidence']
		data_dict = [dict(zip(keys, valuerecord)) for valuerecord in data]

		for i, datum_dict in enumerate(data_dict):
			id  = datum_dict['id']
			if id >= colnum:
				col = {'r': 128, 'g': 128, 'b': 128, 'act': 0}
			else:
				col = {'r': int(colordata[id][0]), 'g': int(colordata[id][1]),  'b': int(colordata[id][2]),  'act': 0}
			data_dict[i].update(col)

		with open( targ.surfaces_segment_info_json_file , 'w') as f:
			json.dump(data_dict, f, indent=2, ensure_ascii=False)

		##
		print('Creating volume data.')
		##
		tp = m.ObtainTileProperty(ref.tile_ids_volume_file)
		wmax = tp['canvas_size_y']
		hmax = tp['canvas_size_x']
		zmax = tp['num_tiles_z']

		## Obtain id volume
		ids_volume = np.zeros([wmax, hmax, zmax], dtype=ref.ids_dtype)
		for iz in range(zmax):
			ids_volume[:,:,iz] = m.ObtainFullSizeIdsPanel(ref.tile_ids_path, ref, tp, iz)

		## Coarsen
		
		print("params['Pitch in X (um)']", params['Pitch in X (um)'])
		print("params['Downsampling factor in X']", params['Downsampling factor in X'])
		
		ph = params['Pitch in X (um)']
		pw = params['Pitch in Y (um)']
		pz = params['Pitch in Z (um)']
		ch = int(params['Downsampling factor in X'])
		cw = int(params['Downsampling factor in Y'])
		cz = int(params['Downsampling factor in Z'])
		ph *= ch
		pw *= cw
		pz *= cz
		ids_volume = ids_volume[::cw,::ch,::cz]
		wmax = ids_volume.shape[0]
		hmax = ids_volume.shape[1]
		zmax = ids_volume.shape[2]

		with h5py.File(targ.volume_file, 'w') as f:		
		    f.create_dataset('volume', data=ids_volume)

		##
		print('Create volume description json file.')
		##
		data_dict = {
		    	'boundingbox_voxel':{
		    		'x': hmax,
		    		'y': wmax,
		    		'z': zmax
		    		},
		    	'boundingbox_um':{
		    		'x': ph * hmax,
		    		'y': pw * wmax,
		    		'z': pz * zmax
		    		},
		    	'pitch_um':{
		    		'x': ph,
		    		'y': pw,
		    		'z': pz
		    		},
				}
		with open( targ.surfaces_volume_description_json_file , 'w') as f:
			json.dump(data_dict, f, indent=2, ensure_ascii=False)

		parent.parent.ExecuteCloseFileFolder(params['Empty Folder for Annotator'])
		parent.parent.OpenFolder(params['Empty Folder for Annotator'])
		print('')
		print('Annotator folder created.')
		print('')
		return True



