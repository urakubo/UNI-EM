
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import math
import h5py
import lxml
import sqlite3
import lxml.etree
import numpy as np
import shutil

from Params import Params
import Miscellaneous as m

class Sego:
    def __init__(self, u_info):

        self.tile_index_w      = 0
        self.tile_num_pixels_y = u_info.tile_num_pixels_y
        self.tile_num_pixels_x = u_info.tile_num_pixels_x
        
        output_path                   = u_info.files_path
        output_ids_path               = u_info.ids_path
        ncolors                       = u_info.ncolors
        
        self.output_tile_ids_path          = u_info.tile_ids_path
        self.output_tile_volume_file       = u_info.tile_ids_volume_file
        self.output_color_map_file         = u_info.color_map_file
        self.output_segment_info_db_file   = u_info.segment_info_db_file

        self.id_max                 = 0
        self.id_counts              = np.array([0], dtype=np.int64 )
        self.id_tile_list           = []
        self.u_info                 = u_info

        self.tile_ids_filename_wzyx = u_info.tile_ids_filename_wzyx
        self.tile_path_wz = u_info.tile_path_wz

        self.id_extension = u_info.id_extension

        # Make a color map
        self.color_map = np.zeros( (ncolors + 1, 3), dtype=np.uint8 )
        for color_i in range( 1, ncolors + 1 ):
            rand_vals = np.random.rand(3)
            self.color_map[ color_i ] = [ rand_vals[0]*255, rand_vals[1]*255, rand_vals[2]*255 ]

    def round(self,shape):
        logs = np.ceil(np.log2(shape)).astype(np.uint32)
        padshape = tuple(2 ** p for p in logs)
        if len(shape) > 2:
            return (shape[0],)+padshape[1:]
        return padshape

    def run(self,input_ids,tile_index_z):

        in_shape = input_ids.shape
        pad_shape = self.round(in_shape)
        original_ids = np.zeros(pad_shape,dtype = input_ids.dtype)
        original_ids[:in_shape[0],:in_shape[1]] = input_ids

        (original_ids_num_pixels_y, original_ids_num_pixels_x) = original_ids.shape ######## ###### 180624Change

        ## Grow regions until there are no boundaries

        current_ids_counts = np.bincount( original_ids.ravel() )
        current_ids_counts_ids = np.nonzero( current_ids_counts )[0]
        current_max = np.max( current_ids_counts_ids )
        self.tile_index_z = tile_index_z

        if self.id_max  < current_max:
            self.id_max  = current_max
            self.id_counts.resize( self.id_max  + 1 )

        self.id_counts[ current_ids_counts_ids ] = self.id_counts[ current_ids_counts_ids ] + np.int64( current_ids_counts [ current_ids_counts_ids ] )

        current_ids_num_pixels_y = original_ids_num_pixels_y
        current_ids_num_pixels_x = original_ids_num_pixels_x
        current_tile_data_space_y  = self.tile_num_pixels_y
        current_tile_data_space_x  = self.tile_num_pixels_x
        self.tile_index_w          = 0
        ids_stride                 = 1

        while current_ids_num_pixels_y > self.tile_num_pixels_y / 2 or current_ids_num_pixels_x > self.tile_num_pixels_x / 2:

            current_tile_ids_path = self.output_tile_ids_path + self.tile_path_wz.format(self.tile_index_w, self.tile_index_z)
            m.mkdir_safe( current_tile_ids_path )

            current_ids = original_ids[ ::ids_stride, ::ids_stride ]

            num_tiles_y = int( math.ceil( float( current_ids_num_pixels_y ) / self.tile_num_pixels_y ) )
            num_tiles_x = int( math.ceil( float( current_ids_num_pixels_x ) / self.tile_num_pixels_x ) )

            print('Scale: ', ids_stride)
            print('Number of panels (x, y): ', num_tiles_x, num_tiles_y)

            for iy in range( num_tiles_y ):
                for ix in range( num_tiles_x ):

                    y = iy * self.tile_num_pixels_y
                    x = ix * self.tile_num_pixels_x

                    current_tile_ids_name    = self.output_tile_ids_path + self.tile_ids_filename_wzyx.format( self.tile_index_w, self.tile_index_z, iy, ix )

                    tile_ids                                                                   = np.zeros( ( self.tile_num_pixels_y, self.tile_num_pixels_x ), np.uint32 )
                    tile_ids_non_padded                                                        = current_ids[ y : y + self.tile_num_pixels_y, x : x + self.tile_num_pixels_x ]
                    tile_ids[ 0:tile_ids_non_padded.shape[0], 0:tile_ids_non_padded.shape[1] ] = tile_ids_non_padded[:,:]

                    if os.path.isfile(current_tile_ids_name) :     ## Backup for undo
                        shutil.move(current_tile_ids_name, current_tile_ids_name+'_')
                        self.u_info.ids_files_undo.extend(current_tile_ids_name)
                    m.save_hdf5( current_tile_ids_name, self.u_info.tile_var_name, tile_ids )

                    for unique_tile_id in np.unique( tile_ids ):

                        self.id_tile_list.append( (unique_tile_id, self.tile_index_w, self.tile_index_z, iy, ix ) )

            current_ids_num_pixels_y = current_ids_num_pixels_y / 2
            current_ids_num_pixels_x = current_ids_num_pixels_x / 2
            current_tile_data_space_y  = current_tile_data_space_y  * 2
            current_tile_data_space_x  = current_tile_data_space_x  * 2
            self.tile_index_w          = self.tile_index_w          + 1
            ids_stride                 = ids_stride                 * 2


    def save(self,in_shape):

        all_shape = self.round(in_shape)
        (numTilesZ, original_ids_num_pixels_y, original_ids_num_pixels_x) = all_shape ###### 180624Change
        
        ## Sort the tile list so that the same id appears together
        self.id_tile_list = np.array( sorted( self.id_tile_list ), np.uint32 )

        ## Write all segment info to a single file

        print('Writing colorMap file (hdf5)')

        hdf5             = h5py.File( self.output_color_map_file, 'w' )

        hdf5['idColorMap'] = self.color_map

        hdf5.close()

        print('Writing segmentInfo file (sqlite)')

        if os.path.exists(self.output_segment_info_db_file):
            os.remove(self.output_segment_info_db_file)
            print("Deleted existing database file.")

        con = sqlite3.connect(self.output_segment_info_db_file)

        cur = con.cursor()

        cur.execute('PRAGMA main.cache_size=10000;')
        cur.execute('PRAGMA main.locking_mode=EXCLUSIVE;')
        cur.execute('PRAGMA main.synchronous=OFF;')
        cur.execute('PRAGMA main.journal_mode=WAL;')
        cur.execute('PRAGMA count_changes=OFF;')
        cur.execute('PRAGMA main.temp_store=MEMORY;')

        cur.execute('DROP TABLE IF EXISTS idTileIndex;')
        cur.execute('CREATE TABLE idTileIndex (id int, w int, z int, y int, x int);')
        cur.execute('CREATE INDEX I_idTileIndex ON idTileIndex (id);')

        cur.execute('DROP TABLE IF EXISTS segmentInfo;')
        cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int);')
        cur.execute('CREATE UNIQUE INDEX I_segmentInfo ON segmentInfo (id);')

        cur.execute('DROP TABLE IF EXISTS relabelMap;')
        cur.execute('CREATE TABLE relabelMap ( fromId int PRIMARY KEY, toId int);')

        for entry_index in range(0, self.id_tile_list.shape[0]):
            values = tuple([str(self.id_tile_list[entry_index, i]) for i in range(5)])
            # print(self.id_tile_list[entry_index, :])
            # print(  values  )
            cur.execute("INSERT INTO idTileIndex VALUES(?, ?, ?, ?, ?);", values )

        taken_names = {}

        for segment_index in range( 1, self.id_max  + 1 ):
            if len( self.id_counts ) > segment_index and self.id_counts[ segment_index ] > 0:
                if segment_index == 0:
                    new_name = '__boundary__'
                else:
                    new_name = "segment{0}".format( segment_index )
                cur.execute('INSERT INTO segmentInfo VALUES(?, ?, ?, ?);', (str(segment_index), str(new_name), str(self.id_counts[ segment_index ]), "0") )

        con.commit()
        con.close()

        #Output TiledVolumeDescription xml file

        print('Writing TiledVolumeDescription file')

        tiledVolumeDescription = lxml.etree.Element( "tiledVolumeDescription",
            fileExtension = self.id_extension,
            numTilesX = str( int( math.ceil( original_ids_num_pixels_x / self.tile_num_pixels_x ) ) ),
            numTilesY = str( int( math.ceil( original_ids_num_pixels_y / self.tile_num_pixels_y ) ) ),
            numTilesZ = str( numTilesZ ),
            numTilesW = str( self.tile_index_w ),
            numVoxelsPerTileX = str( self.tile_num_pixels_x ),
            numVoxelsPerTileY = str( self.tile_num_pixels_y ),
            numVoxelsPerTileZ = str( 1 ),
            numVoxelsX = str( original_ids_num_pixels_x ),
            numVoxelsY = str( original_ids_num_pixels_y ),
            numVoxelsZ = str( numTilesZ ),
            dxgiFormat = 'R32_UInt',
            numBytesPerVoxel = str( 4 ),
            isSigned = str( False ).lower() )

        with open( self.output_tile_volume_file, 'wt' ) as file:
            file.write( lxml.etree.tostring( tiledVolumeDescription, pretty_print = True, encoding="unicode" ) )

