#!/usr/bin/env python
# -*- coding: UTF-8 -*-

##
## Smart merge
##

import os
import sys
import math
import numpy as np
import h5py
import lxml
import lxml.etree
import shutil

from itertools import chain
from typing import Any
from skimage import measure

# sys.path.append("./Filesystem")
# sys.path.append("./../Filesystem")
from np2sego import Sego
from DB import DB
from Params import Params
import Miscellaneous as m
##
##
##

def ObtainFullSizeIds( current_tile_path,  numTilesY, numTilesX, numVoxelsY, numVoxelsX, numVoxelsPerTileY, numVoxelsPerTileX ):
    merged_ids = np.zeros((numVoxelsY, numVoxelsX), np.uint32)  # type: Any
    for tile_index_y in range(numTilesY):
        for tile_index_x in range(numTilesX):
            ## Load panels
            tmp = os.sep + 'y=' + '%08d' % (tile_index_y) + ',' + 'x=' + '%08d' % (tile_index_x) + '.hdf5'
            current_tile_name = current_tile_path + tmp
            tile_ids = load_hdf5(current_tile_name, 'IdMap')

            ## Obtain merged ids
            y = tile_index_y * numVoxelsPerTileY
            x = tile_index_x * numVoxelsPerTileX
            merged_ids[y: y + numVoxelsPerTileY, x: x + numVoxelsPerTileX] = tile_ids
    return  merged_ids

###
###
def main( MergeIDs, UserInfo ):
    ##
    print 'Smart merger activated..'
    ##
    output_tile_ids_path          = UserInfo.tile_ids_path
    output_tile_volume_file       = UserInfo.tile_ids_volume_file
    output_color_map_file         = UserInfo.color_map_file
    output_segment_info_db_file   = UserInfo.segment_info_db_file
    undo_segment_info_db_file     = UserInfo.segment_info_db_undo_file
###
###
    with open( output_tile_volume_file, 'r' ) as file:
        idTiledVolDesc = lxml.etree.parse(file).getroot()
    # "root.tag" and "root.attrib" to check them
    numTilesW 			= int( idTiledVolDesc.get('numTilesW') )			# 1
    numTilesX 			= int( idTiledVolDesc.get('numTilesX') )			# 1
    numTilesY 			= int( idTiledVolDesc.get('numTilesY') )			# 1
    numTilesZ 			= int( idTiledVolDesc.get('numTilesZ') )			# 100
    numVoxelsPerTileX	= int( idTiledVolDesc.get('numVoxelsPerTileX') )	# 512
    numVoxelsPerTileY	= int( idTiledVolDesc.get('numVoxelsPerTileY') )	# 512
    numVoxelsPerTileZ	= int( idTiledVolDesc.get('numVoxelsPerTileZ') )	# 1
    numVoxelsX			= int( idTiledVolDesc.get('numVoxelsX') )			# 512
    numVoxelsY			= int( idTiledVolDesc.get('numVoxelsY') )			# 512
    numVoxelsZ			= int( idTiledVolDesc.get('numVoxelsZ') )			# 100
    ###
    ### Edit IDs
    ###

    flattenMergeIDs = set(chain.from_iterable(MergeIDs))  ## To check whether ids should be updated.
    print flattenMergeIDs
    ids_files_undo  = []

    outfile = Sego(UserInfo)
    tile_index_w = 0
    UserInfo.ids_files_undo = []

    precedent_unified_mask = []
    new_id = []
    for IDs in MergeIDs:
        precedent_unified_mask.append( np.zeros( ( numVoxelsY, numVoxelsX ) , dtype=bool ))
        new_id.append( IDs[0] )  #### To be changed

    for tile_index_z in range(numTilesZ):
        tmp = os.sep + 'w=' + '%08d' % (tile_index_w) + os.sep + 'z=' + '%08d' % (tile_index_z)
        current_tile_path = UserInfo.mojo_tile_ids_path + tmp

        ## Obtain a whole image
        merged_ids = ObtainFullSizeIds( current_tile_path,  numTilesY, numTilesX,
                                        numVoxelsY, numVoxelsX, numVoxelsPerTileY, numVoxelsPerTileX )

        ## Target components for smart connection
        for (iid, IDs) in enumerate(MergeIDs):
            all_labels        = []
            all_num_labels    = []
            all_label_indexes = []
            all_label_areas   = []
            unified_mask = np.zeros( merged_ids.shape , dtype=bool )

            ###
            ### Obtain connected components for each id.
            ###
            for i in range(len(IDs)):
                target_mask           = (merged_ids == IDs[i])           # Obtain target regions.
                target_labels         = measure.label(target_mask)  # Numbering
                target_label_indexes  = np.unique(target_labels)    # Obtain unique
                target_label_indexes  = [j for j in target_label_indexes if j > 0]
                target_label_areas    = [ np.sum(target_labels == j) for j in target_label_indexes]  # Obtain each labeled area

                all_labels.append( target_labels )                  # Label each disconnect area.
                all_num_labels.append(len( target_label_indexes ) ) # Minus baseline
                all_label_indexes.append( target_label_indexes )    # Minus baseline
                all_label_areas.append( target_label_areas )        #
                ##
                unified_mask        = np.logical_or(unified_mask , target_mask)
                ##

            unified_labels        = measure.label(unified_mask)
            unified_label_indexes = np.unique(unified_labels)  # Obtain unique
            unified_label_indexes = [j for j in unified_label_indexes if j > 0]
            unified_label_areas   = [ np.sum(unified_labels == j) for j in unified_label_indexes ]  # Obtain each labeled area

            ###
            ### Operate connection by use of connected components.
            ###
            if sum(all_num_labels) == 0 : # If connected objects were not detected,
                precedent_unified_mask[iid] = np.zeros(merged_ids.shape , dtype=bool)
                continue
            elif sum(all_num_labels) < len( unified_label_indexes ):  #
                print 'Z: ', tile_index_z, ', Num Regions: ', sum(all_num_labels), ', Num Unified Regions: ', len( unified_label_indexes )
                print 'The num of regions is smaller than the num of unified regions. Internal error!'
                return False
            elif sum(all_num_labels) == len( unified_label_indexes ) : # If connected objects were detected,
                merged_ids[unified_mask == True] = new_id[iid]
                outfile.run(merged_ids, tile_index_z)
                precedent_unified_mask[iid] = unified_mask
                continue
            elif sum(all_num_labels) > len( unified_label_indexes ) : # If some connected objects are adjacented.
                print 'Z: ', tile_index_z, ', Num Regions: ', sum(all_num_labels), ', Num Unified Regions: ', len( unified_label_indexes )
                mask_for_connection = np.zeros( merged_ids.shape, dtype=bool )

                ####
                candidates_connected_weights = []
                candidates_connected_mask    = []
                for i in range(len(IDs)):
                    target_labels        = all_labels[i]
                    target_label_areas   = all_label_areas[i]
                    target_label_indexes = all_label_indexes[i]

                    id_connected_target_label_areas  = [j for j in range(len(target_label_areas)) if target_label_areas[j] not in unified_label_areas]
                    id_isolated_target_label_areas   = [j for j in range(len(target_label_areas)) if target_label_areas[j] in unified_label_areas]
                    connected_target_label_indexes   = [ target_label_indexes[j] for j in id_connected_target_label_areas ]
                    isolated_target_label_indexes    = [ target_label_indexes[j] for j in id_isolated_target_label_areas  ]

                    print 'target_label_areas: ', target_label_areas
                    print 'len(target_label_areas): ', len(target_label_areas)
                    print 'connected_target_label_indexes: ', connected_target_label_indexes
                    print 'isolated_target_label_indexes: ', isolated_target_label_indexes

                    ## Connction of isolated areas
                    for k in isolated_target_label_indexes:
                        mask_for_connection = np.logical_or( mask_for_connection,  (target_labels == k) )
                    merged_ids[mask_for_connection == True] = new_id[iid]

                    ## Select the best one from adjacented areas
                    if connected_target_label_indexes != [] :
                        tmp1 = [ np.sum(np.logical_and(precedent_unified_mask[iid] , (target_labels == j) ) ) for j in connected_target_label_indexes ]
                        tmp2 = [ (target_labels == j) for j in connected_target_label_indexes ]
                        candidates_connected_weights.extend(tmp1)
                        candidates_connected_mask.extend(tmp2)


                id = np.argmax( candidates_connected_weights )
                print 'Overlapped area: ', candidates_connected_weights
                print 'Id for largetst overlapped area: ', id
                merged_ids[candidates_connected_mask[id] == True] = new_id[iid]
                outfile.run(merged_ids, tile_index_z)
                precedent_unified_mask[iid] = unified_mask


            ##
            ## Change id files at the specified Z
            ##

            ##

            # Add the Undo functionality
            # print 'Save: ', current_tile_path
            # ids_files_undo.extend(filenames_undo)  ## Filename for undo


    ##
    ## Update database
    ##
    numTilesY_tmp = numTilesY
    numTilesX_tmp = numTilesX

    id_tile_list	= []
    id_max 			= 0
    id_counts       = np.zeros( 0, dtype=np.int64 )


    for tile_index_z in range(numTilesZ):
        numTilesY_tmp = numTilesY
        numTilesX_tmp = numTilesX
        for tile_index_w in range(numTilesW):
            tmp1 = os.sep + 'w=' + '%08d' % (tile_index_w) + os.sep + 'z=' + '%08d' % (tile_index_z)
            current_tile_ids_path = output_tile_ids_path + tmp1
            # print 'Path: ', current_tile_ids_path
            for tile_index_y in range(numTilesY_tmp):
                for tile_index_x in range(numTilesX_tmp):
                    tmp = os.sep + 'y=' + '%08d' % (tile_index_y) + ',' + 'x=' + '%08d' % (tile_index_x) + '.hdf5'
                    current_tile_ids_name = current_tile_ids_path + tmp
                    # print 'Load: ',  current_tile_ids_name
                    tile_ids = load_hdf5(current_tile_ids_name, 'IdMap')
                    unique_tile_ids = np.unique(tile_ids)

                    # print 'Unique IDs: ', unique_tile_ids

                ## Update database
                # Max id
                    current_max = np.max(unique_tile_ids)
                    if id_max < current_max:
                        id_max = current_max
                        id_counts.resize(id_max + 1)
                        # print id_max

                # id list
                    for unique_tile_id in unique_tile_ids:
                        id_tile_list.append((unique_tile_id, tile_index_w, tile_index_z, tile_index_y, tile_index_x))

                # Pixel number of each id
                    current_image_counts = np.bincount(tile_ids.ravel())
                    current_image_counts_ids = np.nonzero(current_image_counts)[0]
                    current_max = np.max(current_image_counts_ids)
                    id_counts[current_image_counts_ids] = \
                        id_counts[current_image_counts_ids] + np.int64(current_image_counts[current_image_counts_ids])

        ##
        ##
            numTilesY_tmp = int( math.ceil( numTilesY_tmp / 2 ) )
            numTilesX_tmp = int( math.ceil( numTilesX_tmp / 2 ) )


    ## print id_counts

    # print id_tile_list

    ## Sort the tile list so that the same id appears together
    id_tile_list = np.array( sorted( id_tile_list ), np.uint32 )

    ## For Undo
    UserInfo.ids_files_undo = ids_files_undo
    UpdateDB.backup( UserInfo, UserInfo.mojo_segment_info_db_undo_file )
    UserInfo.flag_undo      = 1
    UserInfo.flag_redo      = 0

    ## Update database

    UpdateDB.main( output_segment_info_db_file, id_tile_list, id_max, id_counts )
    # print files_ids_undo


# Make a color map
#	ncolors  = id_max + 1
#	color_map = np.zeros( (ncolors + 1, 3), dtype=np.uint8 );
#	for color_i in xrange( 1, ncolors + 1 ):
#		rand_vals = np.random.rand(3);
#		color_map[ color_i ] = [ rand_vals[0]*255, rand_vals[1]*255, rand_vals[2]*255 ];
#
#	print 'Writing colorMap file (hdf5)'
#	hdf5               = h5py.File( output_color_map_file, 'w' )
#	hdf5['idColorMap'] = color_map
#	hdf5.close()


###
###


