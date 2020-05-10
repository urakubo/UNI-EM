##
##
##
import sys, os, time, errno
import numpy as np
import json
import sqlite3
import h5py
import kimimaro


import miscellaneous.Miscellaneous as m
from system.Params import Params

class FolderCreater:
  def __init__( self, u_info, dojo_folder, xpitch, ypitch, zpitch ):
    self.u_info = u_info
    self.dojo_folder = dojo_folder
    self.xpitch = xpitch
    self.ypitch = ypitch
    self.zpitch = zpitch

  def Run(self):
    #print('Annotator folder creater.')
    #return
	##
	## Target dojo file
	##
    tmp_info = Params()
    tmp_info.SetUserInfoAnnotator(self.dojo_folder)
	##
    print('Make directory.')
	##
    if os.path.isdir(tmp_info.surfaces_path) == False:
    	m.mkdir_safe(tmp_info.surfaces_path)
    	m.mkdir_safe(tmp_info.surfaces_whole_path)
    if os.path.isdir(tmp_info.skeletons_path) == False:
    	m.mkdir_safe(tmp_info.skeletons_path)
    	m.mkdir_safe(tmp_info.skeletons_whole_path)

	##
    print('Create database json file.')
	##

	## Load color file
    colordata = m.load_hdf5(tmp_info.annotator_color_map_file, tmp_info.hdf_color_name) 
    colnum = colordata.shape[0];


	## Load database file
    query = "select * from segmentInfo;"
    con = sqlite3.connect(  tmp_info.annotator_segment_info_db_file )
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

    with open( tmp_info.surfaces_segment_info_json_file , 'w') as f:
    	json.dump(data_dict, f, indent=2, ensure_ascii=False)

	##
    print('Create skeletons.')
	##

    ## Load tiledVolumeDescription
    tp = m.ObtainTileProperty(tmp_info.annotator_tile_ids_volume_file)
    xmax = tp['canvas_size_y']
    ymax = tp['canvas_size_x']
    zmax = tp['num_tiles_z']

    ## Obtain id volume
    ids_volume = np.zeros([xmax, ymax, zmax], dtype=tmp_info.ids_dtype)
    for iz in range(zmax):
    	ids_volume[:,:,iz] = m.ObtainFullSizeIdsPanel(tmp_info.annotator_tile_ids_path, tmp_info, tp, iz)

	## Skeletonaization
    skels = kimimaro.skeletonize(
	  ids_volume, 
	  teasar_params={
	    'scale': 4,
	    'const': 500, # physical units
	    'pdrf_exponent': 4,
	    'pdrf_scale': 100000,
	    'soma_detection_threshold': 1100, # physical units
	    'soma_acceptance_threshold': 3500, # physical units
	    'soma_invalidation_scale': 1.0,
	    'soma_invalidation_const': 300, # physical units
	    'max_paths': 50, # default None
	  },
	  # object_ids=[ ... ], # process only the specified labels
	  # extra_targets_before=[ (27,33,100), (44,45,46) ], # target points in voxels
	  # extra_targets_after=[ (27,33,100), (44,45,46) ], # target points in voxels
	  dust_threshold=300, # skip connected components with fewer than this many voxels
	  anisotropy=( self.xpitch, self.ypitch, self.zpitch ), # default True
	  fix_branching=True, # default True
	  fix_borders=True, # default True
	  progress=True, # default False, show progress bar
	  parallel=1, # <= 0 all cpu, 1 single process, 2+ multiprocess
	  parallel_chunk_size=100, # how many skeletons to process before updating progress bar
    )

    skeleton_ids = self._GenerateSkeletonFiles(skels, tmp_info)

	##
    print('Create volume description json file.')
	##

    data_dict = {
	    	'boundingbox_voxel':{
	    		'x': xmax,
	    		'y': ymax,
	    		'z': zmax
	    		},
	    	'boundingbox_um':{
	    		'x': self.xpitch * xmax,
	    		'y': self.ypitch * ymax,
	    		'z': self.zpitch * zmax
	    		},
	    	'pitch_um':{
	    		'x': self.xpitch,
	    		'y': self.ypitch,
	    		'z': self.zpitch
	    		},
	    	'skeleton_ids': skeleton_ids
    		}
    with open( tmp_info.surfaces_volume_description_json_file , 'w') as f:
      json.dump(data_dict, f, indent=2, ensure_ascii=False)

	##
    print('Done.')
    print('Anotator folder generated.')
	##


  def _GenerateSkeletonFiles(self, skels, tmp_info):

    skel_ids = []
    print('Generate skeleton files. Ids are : ')
    for m in skels.keys():
      print(m, end=' ')
      vertices = skels[m].vertices
      edges    = skels[m].edges
      radiuses = skels[m].radius
      skel_ids.append(m)
      filename = tmp_info.skeletons_whole_path + os.sep + str(m).zfill(10)+'.hdf5'
      with h5py.File( filename ,'w') as f:
      	f.create_dataset('vertices', data=vertices)
      	f.create_dataset('edges', data=edges)
      	f.create_dataset('radiuses', data=radiuses)
    print()
    return skel_ids



