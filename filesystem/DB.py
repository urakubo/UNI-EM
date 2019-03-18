####
####
#### DB info, update,
####
####


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sqlite3
import pickle
import shutil
import itertools
import math
import numpy as np
import h5py
import lxml
import lxml.etree
from itertools import chain

from Params import Params
import Miscellaneous as m

class DB :

    def __init__(self, u_info):
        print('DB is loaded.')

        self.u_info = u_info

        with open(u_info.tile_ids_volume_file, 'r') as file:
            id_tiled_vol_desc = lxml.etree.parse(file).getroot()
        # "root.tag" and "root.attrib" to check them
            self.num_tiles_w = int(id_tiled_vol_desc.get('numTilesW'))  # 1
            self.num_tiles_x = int(id_tiled_vol_desc.get('numTilesX'))  # 1
            self.num_tiles_y = int(id_tiled_vol_desc.get('numTilesY'))  # 1
            self.num_tiles_z = int(id_tiled_vol_desc.get('numTilesZ'))  # 100
            self.num_voxels_per_tile_x = int(id_tiled_vol_desc.get('numVoxelsPerTileX'))  # 512
            self.num_voxels_per_tile_y = int(id_tiled_vol_desc.get('numVoxelsPerTileY'))  # 512
            self.num_voxels_per_tile_z = int(id_tiled_vol_desc.get('numVoxelsPerTileZ'))  # 1
            self.num_voxels_x = int(id_tiled_vol_desc.get('numVoxelsX'))  # 512 Import image size
            self.num_voxels_y = int(id_tiled_vol_desc.get('numVoxelsY'))  # 512
            self.num_voxels_z = int(id_tiled_vol_desc.get('numVoxelsZ'))  # 100

            self.canvas_size_x = self.num_tiles_x * self.num_voxels_per_tile_x # 512 Internal image size
            self.canvas_size_y = self.num_tiles_y * self.num_voxels_per_tile_y

        ###
        ### Tile number at each zoom level
        ###
        self.num_tiles_y_at_w = [self.num_tiles_y]
        self.num_tiles_x_at_w = [self.num_tiles_x]
        for iw in range(self.num_tiles_w - 1):
            self.num_tiles_y_at_w.append(int(math.ceil(self.num_tiles_y_at_w[-1] / 2)))
            self.num_tiles_x_at_w.append(int(math.ceil(self.num_tiles_x_at_w[-1] / 2)))

        ###

    def ObtainUpdateIdsInfo(self):
        ###
        id_tile_list = []
        id_max = 0
        id_counts = np.zeros(0, dtype=np.int64)
        for iw in range(self.num_tiles_w):
            for iz, iy, ix in itertools.product(range(self.num_tiles_z), range(self.num_tiles_y_at_w[iw]),
                                            range(self.num_tiles_x_at_w[iw])):

        ### Load tile file
        ### tile_ids( ( tile_num_pixels_y, tile_num_pixels_x ), np.uint32 )

                tile_ids_filename = self.u_info.tile_ids_path + self.u_info.tile_ids_filename_wzyx.format(iw, iz, iy, ix)
                tile_ids = m.load_hdf5(tile_ids_filename, self.u_info.tile_var_name)
                unique_tile_ids = np.unique(tile_ids)

                ## Update database

                # Max id
                current_max = np.max(unique_tile_ids)
                if id_max < current_max:
                    id_max = current_max
                    id_counts.resize(id_max + 1)
                    # print id_max

                # id list
                for unique_tile_id in unique_tile_ids:
                    id_tile_list.append((unique_tile_id, iw, iz, iy, ix))

                # Pixel number of each id
                if iw == 0:
                    current_ids_counts = np.bincount(tile_ids.ravel())
                    current_ids_counts_ids = np.nonzero(current_ids_counts)[0]
                    id_counts[current_ids_counts_ids] = \
                        id_counts[current_ids_counts_ids] + np.int64(current_ids_counts[current_ids_counts_ids])

        ## Sort the tile list so that the same id appears together
        id_tile_list = np.array( sorted( id_tile_list ), np.uint32 )

        ## Max color number check
        if (id_max >= self.u_info.ncolors):
            print('Number of panels exceeds max_number')

        return id_tile_list, id_max, id_counts

###
###
    def Update( self ):

        id_tile_list, id_max, id_counts = self.ObtainUpdateIdsInfo()

        ## Write all segment info to a single file
        print('Writing segmentInfo file (sqlite)')
        con = sqlite3.connect( self.u_info.segment_info_db_file )
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS idTileIndex;')
        cur.execute('CREATE TABLE idTileIndex (id int, w int, z int, y int, x int);')
        cur.execute('CREATE INDEX I_idTileIndex ON idTileIndex (id);')

        for entry_index in range(0, id_tile_list.shape[0]):
            # cur.execute("INSERT INTO idTileIndex VALUES({0}, {1}, {2}, {3}, {4});".format( *id_tile_list[entry_index, :] ))
            values = tuple([str(id_tile_list[entry_index, i]) for i in range(5)])
            # print(  values  )
            cur.execute("INSERT INTO idTileIndex VALUES(?, ?, ?, ?, ?);", values )


        #taken_names = {}
        cur.execute('DROP TABLE IF EXISTS segmentInfo;')
        cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int);')
        cur.execute('CREATE UNIQUE INDEX I_segmentInfo ON segmentInfo (id);')

        for segment_index in range( 1, id_max + 1 ):
            if len( id_counts ) > segment_index and id_counts[ segment_index ] > 0:
                if segment_index == 0:
                    new_name = '__boundary__'
                else:
                    new_name = "segment{0}".format( segment_index )
                # cur.execute('INSERT INTO segmentInfo VALUES({0}, "{1}", {2}, {3});'.format( segment_index, new_name, id_counts[ segment_index ], 0 ))
                cur.execute('INSERT INTO segmentInfo VALUES(?, ?, ?, ?);', (str(segment_index), str(new_name), str(id_counts[segment_index]), '0'))
        con.commit()
        con.close()

###
###
    def Backup( self, segment_info_db_file  ): #  mojo_segment_info_db_backup_file
        con = sqlite3.connect( self.u_info.segment_info_db_file )
        cur = con.cursor()
        cur.execute( 'select * from idTileIndex;' )
        dbdata1 = cur.fetchall()
        cur.execute( 'select * from segmentInfo;' )
        dbdata2 = cur.fetchall()
        con.close()
        with open( segment_info_db_file , 'wb') as f:
            pickle.dump([dbdata1, dbdata2], f)

###
###
    def Restore( self, segment_info_db_backup_file ):

        with open( segment_info_db_backup_file , 'r') as f:
            [dbdata1, dbdata2] = pickle.load(f)

        con = sqlite3.connect( self.u_info.segment_info_db_file )
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS idTileIndex;')
        cur.execute('CREATE TABLE idTileIndex (id int, w int, z int, y int, x int);')
        cur.execute('CREATE INDEX I_idTileIndex ON idTileIndex (id);')
        for entry_index in xrange( len( dbdata1 ) ):
            cur.execute("INSERT INTO idTileIndex VALUES(?, ?, ?, ?, ?);", tuple(dbdata1[entry_index])  )


        initial_or_saved = len(dbdata2[0])
        cur.execute('DROP TABLE IF EXISTS segmentInfo;')
        if initial_or_saved == 4:
            cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int);')
        elif initial_or_saved == 6:
            cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int, type text, subtype text);')

        cur.execute('CREATE UNIQUE INDEX I_segmentInfo ON segmentInfo (id);')
        for entry_index in xrange( len( dbdata2 ) ):
            if initial_or_saved == 4:
                cur.execute("INSERT INTO segmentInfo VALUES(?, ?, ?, ?);", tuple(dbdata2[entry_index])  )
            elif initial_or_saved == 6:
                cur.execute("INSERT INTO segmentInfo VALUES(?, ?, ?, ?, ?, ?);", tuple(dbdata2[entry_index]) )

        con.commit()
        con.close()

###
###
    def ObtainUnusedIdsFromDB( request_num_id ):
        con = sqlite3.connect( self.u_info.segment_info_db_file )
        cur = con.cursor()
        cur.execute( 'select max(id) from segmentInfo;' ) # Obtain max id
        maxid = cur.fetchone()[0]
        cur.execute('select id from segmentInfo;') # Obtain all id list
        usedid = cur.fetchall()
        con.commit() # Update all changes on db
        con.close()

        usedid = set(chain.from_iterable(usedid))     # Obtain list of ids
        all_id = set(range(1, maxid+request_num_id))  # Maxid + necessary id number
        vacant_id   = all_id.difference(usedid)
        vacant_id   = list( vacant_id )
        assigned_id = vacant_id[:request_num_id]
        maxid       = max(assigned_id + [maxid])
        print('Assigned id: ', assigned_id)
        print('Max id: ', maxid)
        if maxid >= self.u_info.ncolors:
            print('Max id exceeds ncolors: ', self.u_info.ncolors)
        return assigned_id, maxid

###
###
