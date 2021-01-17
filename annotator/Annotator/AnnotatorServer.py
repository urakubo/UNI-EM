import socket
import sys, os, time, errno
import tornado
import tornado.websocket
import tornado.httpserver
import asyncio

import numpy as np
import json
import socketio

from skimage import measure
import trimesh
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
    
    super(SurfaceHandler, self).__init__(*args, **kwargs)
  ###
  def get(self):
    id = self.get_argument('id', 'null')
    id = int(id)
    print('Target object id:', id)
    result = self.GenerateStl(id)
    if result :
        self.write("True")
    else :
        self.write("False")
  ###
  def GenerateStl(self, id):
    mask = (self.ids_volume == id)

#    mesher = zmesh.Mesher( tuple(self.pitch) )
#    mesher.mesh( mask )
#    mesh = mesher.get_mesh(1, normals=False)
#    vertices = mesh.vertices
#    faces = mesh.faces 

    try:
        # vertices, normals, faces = march(mask, 2)
        # vertices, faces = mcubes.marching_cubes(mask, 0)
        vertices, faces, normals, values = measure.marching_cubes_lewiner(mask, 0.5, spacing=tuple(self.pitch))
        # print('vertices:', vertices.shape)
        # print('faces   :', faces.shape)
        # verts and normals have x and z flipped because skimage uses zyx ordering
    except:
        print('Mesh was not generated.')
        return False
    # trimesh.constants.tol.merge = 1e-7

    trimesh.constants.tol.merge = 1e-7
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.merge_vertices()
    mesh.remove_degenerate_faces()
    mesh.remove_duplicate_faces()
    print('Processed vertices:', mesh.vertices.shape)
    print('Processed faces   :', mesh.faces.shape)

    # mesh.vertices[:, 0] *= self.pitch[0]
    # mesh.vertices[:, 1] *= self.pitch[1]
    # mesh.vertices[:, 2] *= self.pitch[2]
#    vertices = vertices[:, [2,0,1]]

    filename = os.path.join(self.surfaces_path, str(id).zfill(10)+'.stl')

    #mesh = trimesh.smoothing.filter_humphrey(mesh)
    mesh = trimesh.smoothing.filter_laplacian(mesh, iterations=5)
    #mesh.fill_holes()
    #mesh.export(file_obj=filename,file_type='stl_ascii')
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

    ## Artifact
    coarse_factor = 2
    xpitch *= coarse_factor
    ypitch *= coarse_factor
    self.pitch  = [xpitch, ypitch, zpitch]

	
    ## Obtain id volume
    tp = m.ObtainTileProperty(self.u_info.annotator_tile_ids_volume_file)
    self.ids_volume = np.zeros([xmax, ymax, zmax], dtype=self.u_info.ids_dtype)
    for iz in range(zmax):
    	self.ids_volume[:,:,iz] = m.ObtainFullSizeIdsPanel(self.u_info.annotator_tile_ids_path, self.u_info, tp, iz)
    self.ids_volume = self.ids_volume[::coarse_factor,::coarse_factor,:]

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
      		'surfaces_path': surfaces_whole_path},'skeletons_path': skeletons_whole_path}),
      (r'/socket.io/', socketio.get_tornado_handler(sio)),
      (r'/(.*)', CustomStaticFileHandler, {'path': web_path})
    ],debug=True,autoreload=True)

#      (r'/surface/whole/(.*)', CustomStaticFileHandler, {'path': surfaces_whole_path}),

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

