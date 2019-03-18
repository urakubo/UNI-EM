
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import math
import cv2
import PIL
import PIL.Image
import lxml
import lxml.etree
import numpy as np

from Params import Params
import Miscellaneous as m


class Imgo:
    def __init__(self, u_info):
        self.tile_num_pixels_y = u_info.tile_num_pixels_y
        self.tile_num_pixels_x = u_info.tile_num_pixels_x
        self.output_tile_image_path  = u_info.tile_images_path
        self.output_tile_volume_file = u_info.tile_images_volume_file
        self.tile_images_filename_wzyx = u_info.tile_images_filename_wzyx
        self.tile_path_wz = u_info.tile_path_wz

        self.images_dtype = u_info.images_dtype
        self.image_extension = u_info.image_extension

    def round(self,shape):
        logs = np.ceil(np.log2(shape)).astype(np.uint32)
        padshape = tuple(2 ** p for p in logs)
        # print logs
        if len(shape) > 2:
            return (shape[0],)+padshape[1:]
        return padshape

    def run(self,input_image,tile_index_z):

        in_shape = input_image.shape
        pad_shape = self.round(in_shape)
        original_image = np.zeros(pad_shape,dtype = input_image.dtype)
        original_image[:in_shape[0],:in_shape[1]] = input_image
         
        ( original_image_num_pixels_y, original_image_num_pixels_x ) = original_image.shape ###### 180624Change

        current_image_num_pixels_y = original_image_num_pixels_y
        current_image_num_pixels_x = original_image_num_pixels_x
        current_tile_data_space_y  = self.tile_num_pixels_y
        current_tile_data_space_x  = self.tile_num_pixels_x
        self.tile_index_z          = tile_index_z
        self.tile_index_w          = 0
        images_stride              = 1 ###

        print('Image size (x, y): ', original_image_num_pixels_x, original_image_num_pixels_y)

        while current_image_num_pixels_y > self.tile_num_pixels_y / 2 or current_image_num_pixels_x > self.tile_num_pixels_x / 2:

            current_tile_image_path = self.output_tile_image_path + self.tile_path_wz.format(self.tile_index_w, self.tile_index_z)
            m.mkdir_safe( current_tile_image_path )

#            current_image = cv2.resize(original_image,( current_image_num_pixels_x, current_image_num_pixels_y ))
            current_image = original_image[ ::images_stride, ::images_stride ]

            num_tiles_y = int( math.ceil( float( current_image_num_pixels_y ) / self.tile_num_pixels_y ) )
            num_tiles_x = int( math.ceil( float( current_image_num_pixels_x ) / self.tile_num_pixels_x ) )

            print('Scale: ', images_stride)
            print('Number of panels (x, y): ', num_tiles_x, num_tiles_y)

            for iy in range( num_tiles_y ):
                for ix in range( num_tiles_x ):

                    current_tile_image_name = self.output_tile_image_path + self.tile_images_filename_wzyx.format(self.tile_index_w, self.tile_index_z, iy, ix)

                    y = iy * self.tile_num_pixels_y
                    x = ix * self.tile_num_pixels_x

                    ## tile_image = current_image[y:y + self.tile_num_pixels_y, x:x + self.tile_num_pixels_x]  ###
                    ## m.save_tif8(tile_image, current_tile_image_name ) ###
                    tmp = current_image[y:y + self.tile_num_pixels_y, x:x + self.tile_num_pixels_x]
                    tile_with_fringe = np.zeros((self.tile_num_pixels_y, self.tile_num_pixels_x), self.images_dtype)
                    tile_with_fringe[ 0:tmp.shape[0], 0:tmp.shape[1] ] = tmp
                    m.save_tif8(tile_with_fringe, current_tile_image_name)

                    #print(current_tile_image_name)

            current_image_num_pixels_y = current_image_num_pixels_y / 2
            current_image_num_pixels_x = current_image_num_pixels_x / 2
            current_tile_data_space_y  = current_tile_data_space_y  * 2
            current_tile_data_space_x  = current_tile_data_space_x  * 2
            self.tile_index_w          = self.tile_index_w + 1
            images_stride              = images_stride * 2

    def save(self,in_shape):
        
        all_shape = self.round(in_shape)
        (num_tiles_z, original_image_num_pixels_y, original_image_num_pixels_x) = all_shape ###### 180624Change

        #Output TiledVolumeDescription xml file
        tiledVolumeDescription = lxml.etree.Element( "tiledVolumeDescription",
            fileExtension = self.image_extension,
            numTilesX = str( int( math.ceil( original_image_num_pixels_x / self.tile_num_pixels_x ) ) ),
            numTilesY = str( int( math.ceil( original_image_num_pixels_y / self.tile_num_pixels_y ) ) ),
            numTilesZ = str( num_tiles_z ),
            numTilesW = str( self.tile_index_w ),
            numVoxelsPerTileX = str( self.tile_num_pixels_x ),
            numVoxelsPerTileY = str( self.tile_num_pixels_y ),
            numVoxelsPerTileZ = str( 1 ),
            numVoxelsX = str( original_image_num_pixels_x ),
            numVoxelsY = str( original_image_num_pixels_y ),
            numVoxelsZ = str( num_tiles_z ),
            dxgiFormat = 'R8_UNorm',
            numBytesPerVoxel = str( 1 ),
            isSigned = str( False ).lower() )

        with open( self.output_tile_volume_file, 'wt' ) as file:
            file.write( lxml.etree.tostring( tiledVolumeDescription, pretty_print = True, encoding="unicode" ) )

#    def mkdir_safe(self, dir_to_make ):
#        os.makedirs(dir_to_make)

