import sys, os, time, errno
import numpy as np

from skimage import measure
import trimesh

class GenerateSurface:
  def __init__( self, ids_volume, pitch, surfaces_path):
    self.ids_volume    = ids_volume
    self.pitch         = pitch
    self.surfaces_path = surfaces_path


  ###
  def exec(self, id, smooth_method, num_iter):
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
        v1  = mesh.vertices
        v1center = np.sum(v1,0) / v1.shape[0]
        mesh = trimesh.smoothing.filter_laplacian(mesh, iterations=num_iter)
        v2 = mesh.vertices
        v2center = np.sum(v2,0) / v2.shape[0]
        mesh.vertices += v1center - v2center
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


