#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import itertools
import numpy as np
import h5py
import lxml
import lxml.etree
import tifffile

import PIL
import PIL.Image
import cv2
import png
import csv
import sqlite3

from DB import DB
from Params import Params
import Miscellaneous as m

##
class ExportImgSeg():

    def gen_col_multi(self, data, colordata):
        num_z = data.shape[0]
        num_y = data.shape[1]
        num_x = data.shape[2]
        imgArray = np.zeros((num_z, num_y, num_x, 3), dtype = 'uint8')
        for iz in range(num_z):
            for iy, ix in itertools.product( range(num_y), range(num_x)):
                imgArray[iz, iy, ix, 0] = colordata[data[iz, iy, ix], 0]  # R
                imgArray[iz, iy, ix, 1] = colordata[data[iz, iy, ix], 1]  # G
                imgArray[iz, iy, ix, 2] = colordata[data[iz, iy, ix], 2]  # B
        return imgArray

    ## Export color data as a csv file
    def save_color_data(self, u_info, dir):
        colordata = m.load_hdf5(u_info.color_map_file, u_info.hdf_color_name)
        filename = dir + os.sep + u_info.export_col_name + '.csv'
        print(filename)
        with open(filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(colordata)

    ## Export seg data as a csv file
    def save_segmentInfo(self, u_info, dir):
        con = sqlite3.connect(u_info.segment_info_db_file)
        cur = con.cursor()
        cur.execute('select * from idTileIndex')
        dbdata = cur.fetchall()
        con.close()

        filename = dir + os.sep + u_info.export_db_name + '.csv'
        print(filename)
        with open(filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow( u_info.export_db_ids )
            writer.writerows(dbdata)

    ###
    ###
    def __init__(self):
        pass
    ###
    ###

    def run(self, u_info, dir, fname, ftype, startid, numdigit, flag):

        ## Load DB
        db = DB(u_info)
        print("Tile Num: z {0}, y {1}, x {2}".format(db.num_tiles_z, db.num_tiles_y, db.num_tiles_x))

        ## Makedir
        #self.mkdir_safe(dir)

        ## Save ColorInfo & SegmentationInfo
        if flag == 'ids':
            self.save_color_data(u_info, dir)
            self.save_segmentInfo(u_info, dir)

        ## Volume storage
        VOLUME_FORMAT = ["MTIF16G", "MTIF8G", "MTIF8C","NUMPY32", "NUMPY32C","HDF64"]
        if ftype in VOLUME_FORMAT:
            volume_images_ids = np.zeros((db.num_voxels_z, db.num_voxels_y, db.num_voxels_x), np.uint32)

        ##
        ## Export image/segmentation files
        ##
        print("Tile Num: z {0}, y {1}, x {2}".format(db.num_tiles_z, db.num_tiles_y, db.num_tiles_x))
        iw = 0
        for iz in range(db.num_tiles_z): # 100): # 

            print("iz ", iz)
            merged_images_ids = np.zeros( ( db.canvas_size_y, db.canvas_size_x ), np.uint32 )
            tile_image = []
            for iy, ix in itertools.product( range(db.num_tiles_y), range(db.num_tiles_x)):

                if flag == 'images':
                    filename = u_info.tile_images_path + u_info.tile_images_filename_wzyx.format(iw, iz, iy, ix)
                    print(filename)
                    tile_image = PIL.Image.open(filename)
                elif flag == 'ids' :
                    filename = u_info.tile_ids_path + u_info.tile_ids_filename_wzyx.format(iw, iz, iy, ix)
                    print(filename)
                    tile_image = m.load_hdf5(filename, u_info.tile_var_name)
                else:
                    return False

                y = iy * db.num_voxels_per_tile_y
                x = ix * db.num_voxels_per_tile_x
                merged_images_ids[  y : y + db.num_voxels_per_tile_y, x : x + db.num_voxels_per_tile_x ] = tile_image

            # Crop by original image size
            merged_images_ids = merged_images_ids[  0:db.num_voxels_y, 0:db.num_voxels_x ]

            # Filename setting
            # u_info, dir, fname, ftype, startid, numdigit
            current_frefix = dir + os.sep + fname + str(int(iz+startid)).zfill(numdigit)
            print(current_frefix)
            #

            if ftype in VOLUME_FORMAT:
                volume_images_ids[iz,:,:] = merged_images_ids
            elif ftype == "PNG16G":
                m.save_png16(merged_images_ids, current_frefix+".png")
            elif ftype == "PNG8G":
                m.save_png8(merged_images_ids, current_frefix+".png")
            elif ftype == "PNG8C":
                colordata = m.load_hdf5(u_info.color_map_file, u_info.hdf_color_name)
                m.save_pngc(merged_images_ids, current_frefix+".png", colordata)
            elif ftype == "TIF16G":
                m.save_tif16(merged_images_ids, current_frefix+".tif")
            elif ftype == "TIF8G":
                m.save_tif8(merged_images_ids, current_frefix+".tif")
            elif ftype == "TIF8C":
                colordata = m.load_hdf5(u_info.color_map_file, u_info.hdf_color_name)
                m.save_tifc(merged_images_ids, current_frefix+".tif", colordata)
            else:
                print("Export filetype error (Internal Error).")
        ###
        ###

        current_frefix = dir + os.sep + fname
        print('Save file to ', current_frefix)
        if ftype == "MTIF16G":
            volume_images_ids = volume_images_ids.astype(np.uint16)
            tifffile.imsave(current_frefix + ".tif", volume_images_ids)
        elif ftype == "MTIF8G":
            volume_images_ids = volume_images_ids.astype(np.uint8)
            tifffile.imsave(current_frefix + ".tif", volume_images_ids)
        elif ftype == "MTIF8C":
            print('Multi-tiff 8 color, save.')
            colordata = m.load_hdf5(u_info.color_map_file, u_info.hdf_color_name)
            volume_images_ids = self.gen_col_multi(volume_images_ids, colordata)
            tifffile.imsave(current_frefix + ".tif", volume_images_ids)
        elif ftype == "NUMPY32":
            volume_images_ids = volume_images_ids.astype(np.uint32)
            np.save(current_frefix + ".npy", volume_images_ids)
        elif ftype == "NUMPY32C":
            volume_images_ids = volume_images_ids.astype(np.uint32)
            np.savez(current_frefix + ".npz", stack=volume_images_ids)
        elif ftype == "HDF64":
            volume_images_ids = volume_images_ids.astype(np.int64)
            m.save_hdf5(current_frefix + ".h5", "stack", volume_images_ids)


        print('Images/segmentations were Exported.')

