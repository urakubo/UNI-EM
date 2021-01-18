import socket
import sys, os, time, errno
import numpy as np
import json
import sqlite3
import h5py
import kimimaro

from skimage import measure
import trimesh

class GenerateSkeleton:
  def __init__( self, ids_volume, pitch, skeletons_whole_path):

    self.xpitch = xpitch[0]
    self.ypitch = ypitch[1]
    self.zpitch = zpitch[2]
    self.ids_volume = ids_volume
    self.skeletons_whole_path = skeletons_whole_path

	self.teasar_params={
		'scale': 4,
		'const': 50, # physical units default 500
		'pdrf_exponent': 4,
		'pdrf_scale': 100000,
		'soma_detection_threshold': 1100, # physical units
		'soma_acceptance_threshold': 3500, # physical units
		'soma_invalidation_scale': 1.0,
		'soma_invalidation_const': 300, # physical units
		'max_paths': 50, # default None
		'object_ids': 10}

  def Run( self, id ):
    #mask = (self.ids_volume == id)
	## Skeletonaization
    skels = kimimaro.skeletonize(
	  self.ids_volume, 
	  teasar_params=teasar_params,
	  object_ids=[ id ], # process only the specified labels
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

    skeleton_ids = self._SaveSkeletonFile(skels, id)


  def _SaveSkeletonFile(self, skels, id):

    skel_ids = []
    print('Generate skeleton files. Ids are : ')
    for m in skels.keys():
      print(m, end=' ')
    print('')

	vertices = skels[id].vertices
	edges    = skels[id].edges
	radiuses = skels[id].radius
	filename = self.skeletons_whole_path + os.sep + str(id).zfill(10)+'.hdf5'
	with h5py.File( filename ,'w') as f:
	  	f.create_dataset('vertices', data=vertices)
	  	f.create_dataset('edges', data=edges)
	  	f.create_dataset('radiuses', data=radiuses)
    print()
    return True

