##
## Simple merger
##

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import itertools
import math
import numpy as np
import h5py
import lxml
import lxml.etree
from itertools import chain, product
from skimage import measure
##
## sys.path.append("./Filesystem")
## sys.path.append("./../Filesystem")
from DB import DB
from Params import Params
import Miscellaneous as m
##

###
###
class Merge3DSimple:

    ###
    def __init__(self):
        return
    ###

    ###
    ###
    def run(self, target_ids, u_info):
    ###
    ###
        print('Simple merger runs.')

        ## Load DB
        db = DB(u_info)

        ## Clear undo buffer
        u_info.ids_files_undo = []

        ## Target id
        flatten_target_ids = set(chain.from_iterable(target_ids))

        for iw in range(db.num_tiles_w):
            for iz, iy, ix in product(range(db.num_tiles_z), range(db.num_tiles_y_at_w[iw]), range(db.num_tiles_x_at_w[iw])):

                ### Load tile file
                ### tile_ids( ( tile_num_pixels_y, tile_num_pixels_x ), np.uint32 )
                tile_ids_filename = u_info.tile_ids_path + u_info.tile_ids_filename_wzyx.format( iw, iz, iy, ix )
                tile_ids = m.load_hdf5( tile_ids_filename, u_info.tile_var_name )

                ## Check whether ids should be updated.

                unique_tile_ids = np.unique(tile_ids)
                if bool(flatten_target_ids.intersection( set(unique_tile_ids) ) ):

                    # Backup for undo
                    m.save_hdf5(tile_ids_filename+'_', u_info.tile_var_name, tile_ids)
                    u_info.ids_files_undo.append(tile_ids_filename)

                    # Merge target ids
                    for ids in target_ids:
                        for i in ids:
                            tile_ids[ tile_ids == i ] = ids[0]

                    # Save changes
                    m.save_hdf5( tile_ids_filename, u_info.tile_var_name, tile_ids )
                    print('Save: ', tile_ids_filename)


        ## For Undo
        db.Backup( u_info.segment_info_db_undo_file )
        u_info.flag_undo = 1
        u_info.flag_redo = 0

        ## Update
        db.Update()


###
###


