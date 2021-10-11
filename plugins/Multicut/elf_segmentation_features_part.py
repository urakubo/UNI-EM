import multiprocessing

import numpy as np
import nifty
import nifty.graph.rag as nrag
# import nifty.ground_truth as ngt




# feats.compute_rag
# feats.compute_boundary_feature
# feats.compute_z_edge_mask
# feats.compute_boundary_mean_and_length
# project_node_labels_to_pixels



#
# Region Adjacency Graph and Features
#

def compute_rag(segmentation, n_labels=None, n_threads=None):
    """ Compute region adjacency graph of segmentation.

    Arguments:
        segmentation [np.ndarray] - the segmentation
        n_labels [int] - number of  labels in segmentation.
            If None is give, will be computed from the data. (default: None)
        n_threads [int] - number of threads used, set to cpu count by default. (default: None)
    """
    n_threads = multiprocessing.cpu_count() if n_threads is None else n_threads
    n_labels = int(segmentation.max()) + 1 if n_labels is None else n_labels
    rag = nrag.gridRag(segmentation, numberOfLabels=n_labels,
                       numberOfThreads=n_threads)
    return rag


def compute_boundary_features(rag, boundary_map,
                              min_value=0, max_value=1, n_threads=None):
    """ Compute edge features from boundary map.

    Arguments:
        rag [RegionAdjacencyGraph] - region adjacency graph
        boundary_map [np.ndarray] - boundary map.
        min_value [float] - minimum value used in accumulation (default: 0)
        max_value [float] - maximum value used in accumulation (default: 1)
        n_threads [int] - number of threads used, set to cpu count by default. (default: None)
    """
    n_threads = multiprocessing.cpu_count() if n_threads is None else n_threads
    if tuple(rag.shape) != boundary_map.shape:
        raise ValueError("Incompatible shapes: %s, %s" % (str(rag.shape),
                                                          str(boundary_map.shape)))
    features = nrag.accumulateEdgeStandartFeatures(rag, boundary_map,
                                                   min_value, max_value,
                                                   numberOfThreads=n_threads)
    return features


def compute_affinity_features(rag, affinity_map, offsets,
                              min_value=0, max_value=1, n_threads=None):
    """ Compute edge features from affinity map.

    Arguments:
        rag [RegionAdjacencyGraph] - region adjacency graph
        boundary_map [np.ndarray] - boundary map.
        min_value [float] - minimum value used in accumulation (default: 0)
        max_value [float] - maximum value used in accumulation (default: 1)
        n_threads [int] - number of threads used, set to cpu count by default. (default: None)
    """
    n_threads = multiprocessing.cpu_count() if n_threads is None else n_threads
    if tuple(rag.shape) != affinity_map.shape[1:]:
        raise ValueError("Incompatible shapes: %s, %s" % (str(rag.shape),
                                                          str(affinity_map.shape[1:])))
    if len(offsets) != affinity_map.shape[0]:
        raise ValueError("Incompatible number of channels and offsets: %i, %i" % (len(offsets),
                                                                                  affinity_map.shape[0]))
    features = nrag.accumulateAffinityStandartFeatures(rag, affinity_map, offsets,
                                                       min_value, max_value,
                                                       numberOfThreads=n_threads)
    return features


def compute_boundary_mean_and_length(rag, input_, n_threads=None):
    """ Compute mean value and length of boundaries.

    Arguments:
        rag [RegionAdjacencyGraph] - region adjacency graph
        input_ [np.ndarray] - input map.
        n_threads [int] - number of threads used, set to cpu count by default. (default: None)
    """
    n_threads = multiprocessing.cpu_count() if n_threads is None else n_threads
    if tuple(rag.shape) != input_.shape:
        raise ValueError("Incompatible shapes: %s, %s" % (str(rag.shape),
                                                          str(input_.shape)))
    features = nrag.accumulateEdgeMeanAndLength(rag, input_, numberOfThreads=n_threads)
    return features



#
# Misc
#


def project_node_labels_to_pixels(rag, node_labels, n_threads=None):
    """ Project label values for graph nodes back to pixels to obtain segmentation.

    Arguments:
        rag [RegionAdjacencyGraph] - region adjacency graph
        node_labels [np.ndarray] - array with node labels
        n_threads [int] - number of threads used, set to cpu count by default. (default: None)
    """
    n_threads = multiprocessing.cpu_count() if n_threads is None else n_threads
    if len(node_labels) != rag.numberOfNodes:
        raise ValueError("Incompatible number of node labels: %i, %i" % (len(node_labels),
                                                                         rag.numberOfNodes))
    seg = nrag.projectScalarNodeDataToPixels(rag, node_labels,
                                             numberOfThreads=n_threads)
    return seg


def compute_z_edge_mask(rag, watershed):
    """ Compute edge mask of in-between plane edges for flat superpixels.

    This function does not check wether the input watersheds are
    actually flat!
    """
    node_z_coords = np.zeros(rag.numberOfNodes, dtype='uint32')
    for z in range(watershed.shape[0]):
        node_z_coords[watershed[z]] = z
    uv_ids = rag.uvIds()
    z_edge_mask = node_z_coords[uv_ids[:, 0]] != node_z_coords[uv_ids[:, 1]]
    return z_edge_mask
