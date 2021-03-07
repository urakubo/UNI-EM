#
# Picked up from https://github.com/schlegelp/skeletor/blob/master/skeletor/radiusextraction.py
#

import math
import numbers
import random

import numpy as np
import pandas as pd
import scipy.spatial


import ncollpyde

def get_radius_ray(swc, mesh, n_rays=20, aggregate='mean', 
                   fallback='knn'):
    """Extract radii using ray casting.
    Parameters
    ----------
    swc :           pandas.DataFrame
                    SWC table
    mesh :          trimesh.Trimesh
    n_rays :        int
                    Number of rays to cast for each node.
    aggregate :     "mean" | "median" | "max" | "min" | "percentile75"
                    Function used to aggregate radii for over all intersections
                    for a given node.
    fallback :      "knn" | None | number
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

    assert projection in ['sphere', 'tangents']
    assert (fallback == 'knn') or isinstance(fallback, numbers.Number) or isinstance(fallback, type(None))

    # Get max dimension of mesh
    dim = (swc[['x', 'y', 'z']].max() - swc[['x', 'y', 'z']].min()).values
    radius = max(dim)

    # Vertices for each point on the circle
    points = swc[['x', 'y', 'z']].values
    sources = np.repeat(points, n_rays, axis=0)


	# Ray directions (Simplfied by HU)
    tangents, normals, binormals = frenet_frames(swc)

    v = np.arange(n_rays, dtype=np.float) / n_rays * 2 * np.pi

    all_cx = (radius * -1. * np.tile(np.cos(v), points.shape[0]).reshape((n_rays, points.shape[0]), order='F')).T
    cx_norm = (all_cx[:, :, np.newaxis] * normals[:, np.newaxis, :]).reshape(sources.shape)

    all_cy = (radius * np.tile(np.sin(v), points.shape[0]).reshape((n_rays, points.shape[0]), order='F')).T
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
    final_dist = np.zeros(points.shape[0])
    for l, i in zip(split, np.unique(org_ix)):
        final_dist[i] = agg_func(l)

    if not isinstance(fallback, type(None)):
        # See if any needs fixing
        inside = coll.contains(points)
        is_zero = final_dist == 0
        needs_fix = ~inside | is_zero

        if any(needs_fix):
            if isinstance(fallback, numbers.Number):
                final_dist[needs_fix] = fallback
            elif fallback == 'knn':
                final_dist[needs_fix] = get_radius_kkn(points[needs_fix], mesh, aggregate=aggregate)

    return final_dist

