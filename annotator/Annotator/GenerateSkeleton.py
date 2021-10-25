import sys, os, time, errno
import numpy as np
import h5py
import kimimaro
from scipy import interpolate, spatial
import collections

from skimage import morphology
import trimesh

from annotator.Annotator._get_radius_ray import _get_radius_ray

class GenerateSkeleton:
  def __init__( self, ids_volume, pitch, skeletons_path, surfaces_path, scale, constant, min_voxel, max_path, smooth, extra_after):

    self.xpitch = pitch[0]
    self.ypitch = pitch[1]
    self.zpitch = pitch[2]
    self.ids_volume = ids_volume
    self.skeletons_path = skeletons_path
    self.surfaces_path  = surfaces_path

    self.scale       = scale
    self.constant    = constant
    self.min_voxel   = min_voxel
    self.max_path    = max_path
    self.smooth      = smooth
    self.extra_after = extra_after


  def run( self, id, markerlocs ):

    # mask = (self.ids_volume == id)

	##
	## Markerpoint location correction.
	##
    xmax, ymax, zmax = self.ids_volume.shape

    markerlocs_int_source = [(int(loc[0]/self.xpitch), int(loc[1]/self.ypitch), int(loc[2]/self.zpitch)) for loc in markerlocs]
    markerlocs_int = []

    jmax = 200
    pad_width = ((1,1),(1,1),(1,1))
    #print("markerlocs_int_source: ", markerlocs_int_source)
    if markerlocs_int_source != []:
    	print("Targ ID: ", id)
    	for i, oloc in enumerate(markerlocs_int_source):
    		if self.ids_volume[oloc[0], oloc[1], oloc[2]] == id:
    			markerlocs_int.append( oloc )
    			continue
    		else:
    			j = 0
    			while (j < jmax):
    				outer = morphology.ball(j+1, dtype='bool')
    				inner = np.pad( morphology.ball(j, dtype='bool') , pad_width)
    				ball = np.where(outer ^ inner)
    				j += 1
    				locs = [(ix+oloc[0],iy+oloc[1],iz+oloc[2]) for ix,iy,iz in zip(ball[0], ball[1], ball[2])]
    				#print('j = ', j)
    				for l in locs:
    					if (l[0] < 0) or (l[1] < 0) or (l[2] < 0) or (l[0]>=xmax) or (l[1]>=ymax) or (l[2]>=zmax):
    						continue
    					if self.ids_volume[l[0], l[1], l[2]] == id:
    						markerlocs_int.append( l )
    						j = jmax
    						break

    print("markerlocs_int: ", markerlocs_int)

#    	for i, org_loc in enumerate(markerlocs_int):
#    		print("I and ID", i, self.ids_volume[org_loc[0], org_loc[1], org_loc[2]])

    ##
	## Skeletonaization
	##

    if self.extra_after == True:
    	extra_targets_after  = markerlocs_int
    	extra_targets_before = []
    else :
    	extra_targets_after  = []
    	extra_targets_before = markerlocs_int

    print("Kimimaro initialization...")
    teasar_params={\
		'scale': self.scale,
		'const': self.constant, # physical units default 500
		'pdrf_exponent': 4,
		'pdrf_scale': 100000,
		'soma_detection_threshold': 1100, # physical units
		'soma_acceptance_threshold': 3500, # physical units
		'soma_invalidation_scale': 1.0,
		'soma_invalidation_const': 300, # physical units
		'max_paths': self.max_path}

    skels = kimimaro.skeletonize(
	  self.ids_volume, 
	  teasar_params=teasar_params,
	  object_ids=[ id ], # process only the specified labels
	  #extra_targets_before=markerlocs_int, # target points in voxels
	  extra_targets_after=extra_targets_after, # target points in voxels
	  extra_targets_before=extra_targets_before, # target points in voxels
	  dust_threshold=self.min_voxel, # skip connected components with fewer than this many voxels
	  anisotropy=( self.xpitch, self.ypitch, self.zpitch ), # default True
	  fix_branching=True, # default True
	  fix_borders=True, # default True
	  progress=True, # default False, show progress bar
	  parallel=1, # <= 0 all cpu, 1 single process, 2+ multiprocess
	  parallel_chunk_size=100, # how many skeletons to process before updating progress bar
    )
    # skeleton_ids = self._SaveSkeletonFile(id, vertices, edges, radiuses)

    # vertices = skels[id].vertices
    # edges    = skels[id].edges

    print('skels.keys()   : ', skels.keys())
    print('len(skels)     : ', len(skels) )
    if len(skels) == 0:
    	print('No skeleton. ')
    	return False
    if skels[id].vertices.shape[0] < 4:
    	print('No skeleton. ')
    	return False
    if skels[id].edges.shape[0] < 4:
    	print('No skeleton. ')
    	return False


    vertices = skels[id].vertices
    edges    = skels[id].edges
    # radiuses = skels[id].radius
    if edges.shape[0] < 4:
    	print('No skeleton: ', id)
    	return False

	##
	## Smoothing
	##
    new_vertices, new_edges, new_lengths, new_tangents = self._Smoothing(vertices, edges)

    if new_vertices.shape[0] < 4:
    	print('No skeleton: ', id)
    	return False
    if new_edges.shape[0] < 4:
    	print('No skeleton: ', id)
    	return False

    ##
	## Calculate radiuses for each vartices (k-nearst neighbor)
	##
#    surface_vertices = self._LoadSurfaceVertices(id)
#    tree = spatial.cKDTree(surface_vertices)
#    dists, indexes = tree.query(new_vertices, k=5)
#    new_radiuses	 = np.mean(dists, axis=1)
#    print('new_radiuses: ', new_radiuses.shape)

    ##
	## Calculate radiuses for each vartices (raycaster)
	##
    mesh = self._LoadSurfaceMesh(id)
    new_radiuses	 = _get_radius_ray(new_vertices, new_tangents, mesh)
    print('new_radiuses: ', new_radiuses.shape)

	##
	## Save skeleton
	##
    skeleton_ids = self._SaveSkeletonFile(id, new_vertices, new_edges, new_radiuses, new_lengths, new_tangents)



	##
	## Smoothing
	##

  def _Smoothing(self, vertices, edges):

	# Obtain crossing edges
    edges_ids         = edges.flatten().tolist()
    edges_num_connect = collections.Counter(edges_ids)
    edges_cross = [k for k, v in edges_num_connect.items() if v > 2]

    start_pairs = []
    neighbors_cross = []

	# Obtain the pairs of [crossing edges, neighboring edges]
    for id_cross in edges_cross:
    	tmp = edges[np.any(edges == id_cross, axis=1),:].flatten()
    	_neighbors_cross  = tmp[tmp != id_cross]
#    	print('id_cross: ', id_cross, ', neighbors_cross: ', _neighbors_cross)
    	pairs = [[id_cross, neighbor]  for neighbor in _neighbors_cross]
    	neighbors_cross.extend( _neighbors_cross.tolist() )
    	start_pairs.extend( pairs )

#    print('start_pairs: ',start_pairs)

    flag_used       = np.zeros(len(neighbors_cross))
    neighbors_cross = np.array(neighbors_cross)

	# Track each segment
    segments     = []
    new_segments = []
    for i, pair in enumerate(start_pairs):
    	if flag_used[i] == 0:
    		segment = self._ObtainSegment(pair, edges)
    		segments.append( segment )
    		flag_used += (neighbors_cross == segment[-2])
#    	else:
#    		print("segment already traced.")

#    print('flag_used: ', flag_used)

    num_pts = 200
    large_value = 100000000


	# Set new coordinate
    vertices_list = vertices.tolist()
    new_vertices  = []
    new_lengths   = []
    new_tangents  = []
    new_edges	  = []


    # print('new_lengths : ', new_lengths)

	# Smoothing and mapping of segments
    for segment in segments:
	
		## Smoothing
    	if len(segment) < 4:
    		# print('segment: ', segment)
    		continue
    	x = vertices[segment,0]
    	y = vertices[segment,1]
    	z = vertices[segment,2]
    	w = np.ones(x.shape[0])*10
    	w[0]  = large_value
    	w[-1] = large_value
    	tck, u = interpolate.splprep([x,y,z], s=self.smooth, w=w ) # s = 50
    	u_fine = np.linspace(0,1,num_pts)
    	x_fit, y_fit, z_fit = interpolate.splev(u_fine, tck)
    	
    	## Segmental lengths
    	x_diff = np.diff(x_fit)
    	y_diff = np.diff(y_fit)
    	z_diff = np.diff(z_fit)
    	tmp_len     = np.sqrt(x_diff*x_diff + y_diff*y_diff + z_diff*z_diff)
    	tmp_lengths = np.append(tmp_len, 0)/2 + np.append(0,tmp_len)/2
    	tmp_lengths = tmp_lengths.tolist()
    	# print('tmp_lengths: ', tmp_lengths)
    	
    	## Segmental tangents
    	tmp_tangents = np.stack((x_diff, y_diff, z_diff))
    	tmp_tangents /= tmp_len
    	tmp_tangents = tmp_tangents.T
    	tmp_tangents = np.vstack( [tmp_tangents, tmp_tangents[-1,:].reshape(1,3)] )

		## Mapping
    	tmp_verts = [[ix,iy,iz] for ix,iy,iz in zip(x_fit, y_fit, z_fit) ]
    	ids_start_new = len(new_vertices)
    	new_vertices.extend(tmp_verts)
    	new_lengths.extend(tmp_lengths)
    	new_tangents.extend(tmp_tangents)
    	ids_end_new = len(new_vertices)
    	tmp_edges = [[i, i+1] for i in range(ids_start_new,ids_end_new-1)]
    	new_edges.extend(tmp_edges)
	
    new_vertices      = np.array(new_vertices)
    new_edges		  = np.array(new_edges)
    new_lengths  	  = np.array(new_lengths)
    new_tangents	  = np.array(new_tangents)
    print('Vertices: ', new_vertices.shape)
    print('Edges   : ', new_edges.shape)
    print('Lengths : ', new_lengths.shape)
    print('Tangents: ', new_tangents.shape)

    return new_vertices, new_edges, new_lengths, new_tangents


  def _LoadSurfaceVertices(self, id):
    print('Loading surface, ID: ', id)
    filename = self.surfaces_path + os.sep + str(id).zfill(10)+'.stl'
    mesh = trimesh.load(filename)
    vertices = mesh.vertices
    print('')
    return vertices

  def _LoadSurfaceMesh(self, id):
    print('Loading surface, ID: ', id)
    filename = self.surfaces_path + os.sep + str(id).zfill(10)+'.stl'
    mesh = trimesh.load(filename)
    print('')
    return mesh


  def _SaveSkeletonFile(self, id, vertices, edges, radiuses, lengths, tangents):
    filename = self.skeletons_path + os.sep + str(id).zfill(10)+'.hdf5'
    with h5py.File( filename ,'w') as f:
    	f.create_dataset('vertices', data=vertices)
    	f.create_dataset('edges'   , data=edges)
    	f.create_dataset('radiuses', data=radiuses)
    	f.create_dataset('lengths' , data=lengths)
    	f.create_dataset('tangents', data=tangents)
    print('Generated skeleton ID: ', id)
    print('')
    return True


  def _ObtainSegment(self, start_pair, edges):
    output_edges = start_pair # list
    while True:
    	tmp = edges[np.any(edges == output_edges[-1], axis=1),:]
    	tmp = tmp[np.all(tmp != output_edges[-2], axis=1),:]
    	if (tmp.shape[0] == 1):
    		newid = tmp[tmp != output_edges[-1]].tolist()
    		output_edges.extend(newid)
    	else:
    		return output_edges

