###
###
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import itertools
import math
import numpy as np
import shutil

from time import sleep

from DB import DB
from Params import Params
import Miscellaneous as m

import tornado.websocket
import tornado.httpserver
import threading

from os import path, pardir
current_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
#sys.path.append(parent_dir)

#from DojoStandalone import ServerLogic
import DojoStandalone


#import h5py
#import lxml
#import lxml.etree

class SaveChanges:

    ###
    def __init__(self):
        return
    ###
    def lookup_label(self, label_id, merge_table):

        while str(label_id) in merge_table.keys():
            label_id = merge_table[str(label_id)]
        return label_id

    ###

    def StartThreadDojo(self):
        logic = DojoStandalone.ServerLogic()
        logic.run(self.u_info)

    ###
    ###
    def run(self, u_info):

        ## Load DB
        db = DB(u_info)
        self.u_info = u_info
        ##
        ## Update split and adjust
        ##

        for iz in range(db.num_tiles_z):

            print('Saving: ', iz, '/', db.num_tiles_z)
            # Check teemporary data
            data_path = u_info.tmp_tile_ids_path + u_info.tile_path_wz.format(0, iz)
            if not os.path.isdir(data_path):
                continue

            # print('Copy from ', data_path)
            for iw in range(db.num_tiles_w):
                source_dir = u_info.tmp_tile_ids_path \
                                 + u_info.tile_path_wz.format(iw, iz)
                destination_dir = u_info.tile_ids_path \
                                      + u_info.tile_path_wz.format(iw, iz)
                shutil.rmtree(destination_dir)
                shutil.move(source_dir, destination_dir)

                ## Remove temp file
                # shutil.rmtree(source_dir)

        ##
        ## Update merges
        ##

        # print(u_info.merge_table)

        for iw in range(db.num_tiles_w):
            for iz, iy, ix in itertools.product(range(db.num_tiles_z), range(db.num_tiles_y_at_w[iw]), range(db.num_tiles_x_at_w[iw])):

                ### Load tile file
                tile_ids_filename = u_info.tile_ids_path + u_info.tile_ids_filename_wzyx.format( iw, iz, iy, ix )
                tile_ids = m.load_hdf5( tile_ids_filename, u_info.tile_var_name )

                ## Color exchange [for merge? check __merge_table.keys() ]
                for mm in u_info.merge_table.keys():
                    mm_id = self.lookup_label(mm, u_info.merge_table)
                    tile_ids[ tile_ids == int(mm) ] = mm_id

                ### Save tile file
                    m.save_hdf5(tile_ids_filename, u_info.tile_var_name, tile_ids)

        u_info.merge_table = {}
        u_info.flag_undo = 0
        u_info.flag_redo = 0

        ## Update
        print('Updating database.')
        db.Update()
        print('Successfully saved.')


