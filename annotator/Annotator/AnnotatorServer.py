import socket
import sys, os, time, errno
import tornado
import tornado.websocket
import tornado.httpserver
import tornado.escape
import asyncio

import numpy as np
import json
import socketio

from skimage import measure
import trimesh
import h5py

# from marching_cubes import march
# import mcubes
# import zmesh


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "system"))

from Params import Params
from annotator.Annotator.sio import sio, set_u_info
import miscellaneous.Miscellaneous as m
from annotator.Annotator.GenerateSkeleton import GenerateSkeleton


class CustomStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-cache')


class SurfaceSkeletonHandler(tornado.web.RequestHandler):
  ###
  def __init__(self, *args, **kwargs):
    self.ids_volume	= kwargs.pop('3Dmap')
    self.pitch		= kwargs.pop('pitch')
    self.surfaces_path  = kwargs.pop('surfaces_path')
    self.skeletons_path = kwargs.pop('skeletons_path')
    
    super(SurfaceSkeletonHandler, self).__init__(*args, **kwargs)

  ###
  def prepare(self):
    if self.request.headers.get('Content-Type') != 'application/json':
    	raise HTTPError(406)

  ###
  def post(self, *arg, **kwargs):
    request = tornado.escape.json_decode(self.request.body)
    if 'mode' not in request:
    	print('Bad request: ', request)
    	self.write("False")
    	return False

    print('\n'.join("  {}: {}".format(k, v) for k, v in request.items()))
    if request['mode'] == 'surface':
#    	print( str(request['smooth_method']) )
#    	print( str(request['num_iter']) )
    	id 				= int(request['id'])
    	smooth_method 	= str(request['smooth_method'])
    	num_iter 		= int(request['num_iter'])

    	# print('Target object id:', id)
    	result = self.generate_surface(id, smooth_method, num_iter)
    	if result :
    		self.write("True")
    	else :
    		self.write("False")

    elif request['mode'] == 'skeleton':
#    	print('Request skeleton: ')
    	scale     = int(request['scale'])
    	constant  = int(request['constant'])
    	min_voxel = int(request['min_voxel'])
    	max_path  = int(request['max_path'])
    	smooth    = int(request['smooth'])
    	gen_skel = GenerateSkeleton(self.ids_volume, self.pitch, self.skeletons_path, self.surfaces_path,\
    		scale, constant, min_voxel, max_path, smooth)
    	for elem in request['element']:
	    	# print('Skeleton: ', elem )
	    	result = gen_skel.run(elem['id'], elem['markerlocs'])
	    	if not result :
	    		self.write("False")
    	self.write("True")

    else :
    	print('Bad request: ', request)
    	self.write("False")
    	return False

  ###
  def generate_surface(self, id, smooth_method, num_iter):
    mask = (self.ids_volume == id)
    try:
        if 'marching_cubes' in dir(measure):
            vertices, faces, normals, values = measure.marching_cubes(mask, level=0.5, spacing=tuple(self.pitch),gradient_direction='ascent')
        elif 'marching_cubes_lewiner' in dir(measure):
            vertices, faces, normals, values = measure.marching_cubes_lewiner(mask, level=0.5, spacing=tuple(self.pitch),gradient_direction='ascent')
        vertices = vertices - self.pitch
        # Parameters: spacing : length-3 tuple of floats
        # Voxel spacing in spatial dimensions corresponding to numpy array
        # indexing dimensions (M, N, P) as in `volume`.
        # Returns: verts : (V, 3) array matches input `volume` (M, N, P).
        #
        # ??? verts and normals have x and z flipped because skimage uses zyx ordering
        # vertices = vertices[:, [2,0,1]]
    except:
        print('Mesh was not generated.')
        return False
#    trimesh.constants.tol.merge = 1e-7
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.merge_vertices()
    mesh.remove_degenerate_faces()
    mesh.remove_duplicate_faces()
    if smooth_method == "Humphrey":
        mesh = trimesh.smoothing.filter_humphrey(mesh, iterations=num_iter)
        # print("Humphrey filter with ", num_iter, " iterations")
    elif smooth_method == "Laplacian":
        mesh = trimesh.smoothing.filter_laplacian(mesh, iterations=num_iter)
        # print("Laplacian filter with ", num_iter, " iterations")
    elif smooth_method == "Taubin":
        mesh = trimesh.smoothing.filter_taubin(mesh, iterations=num_iter)
        # print("Taubin filter with ", num_iter, " iterations")
    else :
        pass
        # print("No smoothing.")
        # print("No smoothing.")

    print('Processed vertices:', mesh.vertices.shape)
    print('Processed faces   :', mesh.faces.shape)

    filename = os.path.join(self.surfaces_path, str(id).zfill(10)+'.stl')
    mesh.export(file_obj=filename)
    return True

  ###
class AnnotatorServerLogic:
  def __init__( self, u_info  ):
    ## User info
    self.u_info = u_info

	## Load volume_description
    with open(self.u_info.surfaces_volume_description_json_file, 'r') as f:
      volume_description = json.load(f)

    xpitch = volume_description['pitch_um']['x']
    ypitch = volume_description['pitch_um']['y']
    zpitch = volume_description['pitch_um']['z']
    xmax	= volume_description['boundingbox_voxel']['x']
    ymax	= volume_description['boundingbox_voxel']['y']
    zmax	= volume_description['boundingbox_voxel']['z']
    self.pitch  = [xpitch, ypitch, zpitch]

    ## Load volume file
    with h5py.File(self.u_info.volume_file, 'r') as f:		
      self.ids_volume = f['volume'][()]

#    print('self.ids_volume.shape: ', self.ids_volume.shape)
    return None


  def run( self ):
    ####
    web_path = os.path.join(self.u_info.web_annotator_path, "dist")
    skeletons_path  = self.u_info.skeletons_path
    surfaces_path   = self.u_info.surfaces_path
    skeletons_whole_path = self.u_info.skeletons_whole_path
    surfaces_whole_path  = self.u_info.surfaces_whole_path

    ####
    paint_path  = self.u_info.paint_path
    ####
    ev_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ev_loop)

    set_u_info(self.u_info)

    annotator = tornado.web.Application([
      (r'/surface/(.*)', CustomStaticFileHandler, {'path': surfaces_path}),
      (r'/skeleton/(.*)', CustomStaticFileHandler, {'path': skeletons_path}),
      (r'/ws/surface_skeleton', SurfaceSkeletonHandler, {'3Dmap': self.ids_volume, 'pitch': self.pitch,
      		'surfaces_path': surfaces_whole_path,'skeletons_path': skeletons_whole_path}),
      (r'/socket.io/', socketio.get_tornado_handler(sio)),
      (r'/(.*)', CustomStaticFileHandler, {'path': web_path})
    ],debug=True,autoreload=True)


    server = tornado.httpserver.HTTPServer(annotator)
    server.listen(self.u_info.port_annotator)
    print('*'*80)
    print('*', '3D Annotator RUNNING')
    print('*')
    print('*', 'open', '[ ' + self.u_info.url_annotator  + 'index.html ] ')
    print('*'*80)

    tornado.ioloop.IOLoop.instance().start()
    #ev_loop.stop()
    #ev_loop.close()
    #server.stop()
    print("Tornado web server stops.")
    return


  def stop():
    print("Called stop")
    asyncio.asyncio_loop.stop()
    server.stop()


  def close(self, signal, frame):
    print('Sayonara..!!')
    sys.exit(0)

