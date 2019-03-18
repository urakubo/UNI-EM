#!/usr/bin/env python
# -*- coding: UTF-8 -*-

##
## Smart merge
##

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import math
import numpy as np
import h5py
import lxml
import lxml.etree
import shutil
import pickle
import cv2
import sqlite3

from itertools import chain
# import UpdateDB
from typing import Any
from np2sego import Sego
from skimage import measure


from DB import DB
from Params import Params
import Miscellaneous as m

###
###
class Disconnect3D:


###
###
    def __init__(self, disconnect_id, u_info):

        ## Nortification
        print('3D disconnector runs.')

        ## Load DB
        db = DB(u_info)

        ## Clear undo buffer
        u_info.ids_files_undo = []

        ## Obtain a target region as a bool 3d array
        mask = np.zeros( ( db.canvas_size_y, db.canvas_size_x,  db.num_tiles_z ) , dtype=bool )
        for iz in range(db.num_tiles_z):
            full_map = m.ObtainFullSizeIdsPanel(u_info, db, iz)
            mask[:, :, iz] = (full_map == disconnect_id)

        ## Obtain disconnect regions by use of "measure.label"
        labels, num_labels = measure.label(mask, neighbors=4, return_num=True) # "labels" will require large memory.
        print('Number of disconnected components: ', num_labels)


        ## Assign new ids
        assigned_id, maxid = db.ObtainUnusedIdsFromDB(u_info, num_labels - 1)

        ## Make changes on files
        ## Original images

        for iz in range(db.num_tiles_z):
            # Resize ids
            for iw in range(db.num_tiles_w):
                current_num_voxels_y = db.num_tiles_y_at_w[iw] * db.num_voxels_per_tile_y
                current_num_voxels_x = db.num_tiles_x_at_w[iw] * db.num_voxels_per_tile_x

                targ = labels[::(2 ** iw), ::(2 ** iw), iz]
                current_labels = zeros((current_num_voxels_y, current_num_voxels_x), targ.dtype)
                current_labels[0:targ.shape[0], 0:targ.shape[1]] = targ

                for iy, ix in itertools.product(range(db.num_tiles_y_at_w[iw]),
                                                range(db.num_tiles_x_at_w[iw])):
                    ## Obtain a target id panel
                    yid_start  = iy * db.num_voxels_per_tile_y
                    xid_start  = ix * db.num_voxels_per_tile_x
                    yid_goal   = iy * db.num_voxels_per_tile_y + db.num_voxels_per_tile_y
                    xid_goal   = ix * db.num_voxels_per_tile_x + db.num_voxels_per_tile_x
                    tmp_labels = current_labels[yid_start: yid_goal, xid_start: xid_goal, iz]

                    if np.max(tmp_labels) > 0:
                        ## Obtain the target tile
                        tile_ids_filename = u_info.mojo_tile_ids_path \
                            + u_info.tile_ids_filename_wzyx.format(iw, iz, iy, ix)
                        tile_ids = m.load_hdf5(tile_ids_filename, u_info.tile_var_name)

                        # Backup undo
                        m.save_hdf5(tile_ids_filename + '_', u_info.tile_var_name, tile_ids)
                        ids_files_undo.append(tile_ids_filename)  ## Filename for undo

                        # Make changes
                        for i in range(num_labels) :
                            tile_ids[tmp_labels == i+1] = assigned_id[i]
                        m.save_hdf5(tile_ids_filename, u_info.tile_var_name, tile_ids)


        ##
        ## Update database
        ##

        ## For Undo
        db.Backup(u_info.segment_info_db_undo_file)
        u_info.flag_undo = 1
        u_info.flag_redo = 0

        ## Update
        db.Update(u_info)


    ## outfile = Sego(u_info)
    ## outfile.run(merged_ids, tile_index_z)




###
###


