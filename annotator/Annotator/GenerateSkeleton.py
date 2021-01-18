import sys, os, time, errno
import numpy as np
import h5py
import kimimaro
from scipy import interpolate
import collections

class GenerateSkeleton:
  def __init__( self, ids_volume, pitch, skeletons_whole_path):

    self.xpitch = pitch[0]
    self.ypitch = pitch[1]
    self.zpitch = pitch[2]
    self.ids_volume = ids_volume
    self.skeletons_whole_path = skeletons_whole_path

    self.teasar_params={\
		'scale': 4,
		'const': 50, # physical units default 500
		'pdrf_exponent': 4,
		'pdrf_scale': 100000,
		'soma_detection_threshold': 1100, # physical units
		'soma_acceptance_threshold': 3500, # physical units
		'soma_invalidation_scale': 1.0,
		'soma_invalidation_const': 300, # physical units
		'max_paths': 50}

  def Run( self, id ):
    #mask = (self.ids_volume == id)
	## Skeletonaization
    skels = kimimaro.skeletonize(
	  self.ids_volume, 
	  teasar_params=self.teasar_params,
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

	##
	## Smoothing
	##

    vertices = skels[id].vertices
    edges    = skels[id].edges
    radiuses = skels[id].radius

	edges_ids         = edges.flatten().tolist()
	edges_num_connect = collections.Counter(edges_ids)
	edges_end   = [k for k, v in edges_num_connect.items() if v == 1]
	edges_cross = [k for k, v in edges_num_connect.items() if v > 2]
	edges_end.extend(edges_cross)

	start_edge_pairs = []
	start_edge_solo  = []

	for id_cross in edges_cross:
		tmp = edges[np.any(edges == id_cross, axis=1),:]
		tmp_ = tmp.flatten()
		start_points  = tmp_[tmp_ != id_cross]
		base_crossing = np.ones(start_points.shape).astype(int)*id_cross
		tmp__ = np.vstack([base_crossing, start_points]).transpose()
		start_edge_solo.extend( start_points.tolist() )
		start_edge_pairs.extend( tmp__.tolist() )

	start_edge_solo = np.array(start_edge_solo)

	cross_flag      = np.zeros(start_edge_solo.shape)
	segments = []
	for i in range(len(start_edge_pairs)):
		if cross_flag[i] == 0 :
			segment = obtain_segment(start_edge_pairs[i], edges)
			segments.append( segment )
			cross_flag = cross_flag + (start_edge_solo == segment[-2])

	num_pts = 200
	large_value = 100000000
	#fig2 = plt.figure(2)
	#ax3d = fig2.add_subplot(111, projection='3d')
	for segment in segments:
		if len(segment) < 4:
			print('segment: ', segment)
			continue
		x = vertices[segment,0]
		y = vertices[segment,1]
		z = vertices[segment,2]
		w = np.ones(x.shape[0])*10
		w[0]  = large_value
		w[-1] = large_value
		
		tck, u = interpolate.splprep([x,y,z], s=4, w=w )
		u_fine = np.linspace(0,1,num_pts)
		x_fit, y_fit, z_fit = interpolate.splev(u_fine, tck)


	# Save skeleton
    skeleton_ids = self._SaveSkeletonFile(skels, id)


  def _SaveSkeletonFile(self, skels, id):

    skel_ids = []
    print('Generate skeleton ids: ')
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
    print('Generated', id)
    return True



def _ObtainSegment(start_pair, edges):
	output_edges = start_pair # list
	while True:
		tmp = edges[np.any(edges == output_edges[-1], axis=1),:]
		tmp = tmp[np.all(tmp != output_edges[-2], axis=1),:]
		if (tmp.shape[0] == 1):
			newid = tmp[tmp != output_edges[-1]].tolist()
			output_edges.extend(newid)
		else:
			return output_edges

