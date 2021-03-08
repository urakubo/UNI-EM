#
# Modified up from https://github.com/schlegelp/skeletor/blob/master/skeletor/radiusextraction.py
#

import math
import numbers
import random

import numpy as np

import ncollpyde

def _get_radius_ray(vertices, tangents, mesh, n_rays=20, aggregate='mean', fallback=0):
    """Extract radii using ray casting.
    Parameters
    ----------
    vertices :      (N,3) numpy
    mesh :          trimesh.Trimesh
    n_rays :        int
                    Number of rays to cast for each node.
    aggregate :     "mean" | "median" | "max" | "min" | "percentile75"
                    Function used to aggregate radii for over all intersections
                    for a given node.
    fallback :      None | number
                    If a point is outside or right on the surface of the mesh
                    the raycasting will return nonesense results. We can either
                    ignore those cases (``None``), assign a arbitrary number or
                    we can fall back to radii from k-nearest-neighbors (``knn``).
    Returns
    -------
    radii :     np.ndarray
                Corresponds to input coords.
    """
    agg_map = {'mean': np.mean, 'max': np.max, 'min': np.min,
               'median': np.median, 'percentile75': lambda x: np.percentile(x, 75)}
    assert aggregate in agg_map
    agg_func = agg_map[aggregate]

    assert isinstance(fallback, numbers.Number) or isinstance(fallback, type(None))

    # Get max dimension of mesh
    xmaxdist = max(vertices[:,0]) -min(vertices[:,0])
    ymaxdist = max(vertices[:,1]) -min(vertices[:,1])
    zmaxdist = max(vertices[:,2]) -min(vertices[:,2])
    radius = max([xmaxdist, ymaxdist, zmaxdist])

    # Vertices for each point on the circle
    sources = np.repeat(vertices, n_rays, axis=0)


	# Ray directions (Simplfied by HU)
    normals, binormals = get_normals(tangents)
    # tangent is not used. normals and binormals are used.

    v = np.arange(n_rays, dtype=np.float) / n_rays * 2 * np.pi

    all_cx = (radius * -1. * np.tile(np.cos(v), vertices.shape[0]).reshape((n_rays, vertices.shape[0]), order='F')).T
    cx_norm = (all_cx[:, :, np.newaxis] * normals[:, np.newaxis, :]).reshape(sources.shape)

    all_cy = (radius * np.tile(np.sin(v), vertices.shape[0]).reshape((n_rays, vertices.shape[0]), order='F')).T
    cy_norm = (all_cy[:, :, np.newaxis] * binormals[:, np.newaxis, :]).reshape(sources.shape)

    targets = sources + cx_norm + cy_norm

    # Initialize ncollpyde Volume
    coll = ncollpyde.Volume(mesh.vertices, mesh.faces, validate=False)

    # Get intersections: `ix` points to index of line segment; `loc` is the
    #  x/y/z coordinate of the intersection and `is_backface` is True if
    # intersection happened at the inside of a mesh
    ix, loc, is_backface = coll.intersections(sources, targets)

    # Remove intersections with front faces
    # For some reason this reduces the number of intersections to 0 for many
    # points
    #ix = ix[~is_backface]
    #loc = loc[~is_backface]

    # Calculate intersection distances
    dist = np.sqrt(np.sum((sources[ix] - loc)**2, axis=1))

    # Map from `ix` back to index of original point
    org_ix = (ix / n_rays).astype(int)

    # Split by original index
    split_ix = np.where(org_ix[:-1] - org_ix[1:])[0]
    split = np.split(dist, split_ix)

    # Aggregate over each original ix
    final_dist = np.zeros(vertices.shape[0])
    for l, i in zip(split, np.unique(org_ix)):
        final_dist[i] = agg_func(l)

    if not isinstance(fallback, type(None)):
        # See if any needs fixing
        inside = coll.contains(vertices)
        is_zero = final_dist == 0
        needs_fix = ~inside | is_zero
        final_dist[needs_fix] = 0

    return final_dist





def get_normals(tangents):
    """Calculate tangents, normals and binormals for each parent->child segment."""

    normals = np.zeros_like(tangents)

    epsilon = 0.0001

    mags = np.sqrt(np.sum(tangents * tangents, axis=1))
    tangents /= mags[:, np.newaxis]

    # Get initial normal and binormal
    t = np.abs(tangents[0])

    smallest = np.argmin(t)
    normal = np.zeros(3)
    normal[smallest] = 1.

    vec = np.cross(tangents[0], normal)
    normals[0] = np.cross(tangents[0], vec)

    all_vec = np.cross(tangents[:-1], tangents[1:])
    all_vec_norm = np.linalg.norm(all_vec, axis=1)

    # Normalise vectors if necessary
    where = all_vec_norm > epsilon
    all_vec[where, :] /= all_vec_norm[where].reshape((sum(where), 1))

    # Precompute inner dot product
    dp = np.sum(tangents[:-1] * tangents[1:], axis=1)
    # Clip
    cl = np.clip(dp, -1, 1)
    # Get theta
    th = np.arccos(cl)

    # Compute normal and binormal vectors along the path
    for i in range(1, tangents.shape[0]):
        normals[i] = normals[i-1]

        vec_norm = all_vec_norm[i-1]
        vec = all_vec[i-1]
        if vec_norm > epsilon:
            normals[i] = rotate(-np.degrees(th[i-1]),
                                vec)[:3, :3].dot(normals[i])

    binormals = np.cross(tangents, normals)

    return normals, binormals



def rotate(angle, axis):
    """Construct 3x3 rotation matrix for rotation about a vector.
    Parameters
    ----------
    angle : float
            The angle of rotation, in degrees.
    axis :  ndarray
            The x, y, z coordinates of the axis direction vector.
    Returns
    -------
    M :     ndarray
            Transformation matrix describing the rotation.
    """
    angle = np.radians(angle)
    assert len(axis) == 3
    x, y, z = axis / np.linalg.norm(axis)
    c, s = math.cos(angle), math.sin(angle)
    cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z
    M = np.array([[cx * x + c, cy * x - z * s, cz * x + y * s, .0],
                  [cx * y + z * s, cy * y + c, cz * y - x * s, 0.],
                  [cx * z - y * s, cy * z + x * s, cz * z + c, 0.],
                  [0., 0., 0., 1.]]).T
    return M


