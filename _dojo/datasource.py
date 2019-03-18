from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import re

import h5py
import json
import xml.etree.ElementTree as ET

import cv2

from database import Database

class Datasource(object):

  def __init__(self, mojo_dir, tmp_dir, query, input_format, output_format, sub_dir):


    self.__mojo_dir = mojo_dir
    self.__mojo_tmp_dir = tmp_dir

    self.__query = query
    self.__input_format = input_format
    self.__output_format = output_format
    self.__sub_dir = sub_dir

#    self.__out_dir = out_dir

    # {'numBytesPerVoxel': '4', 'numVoxelsPerTileZ': '1', 'numVoxelsX': '1024', 'numVoxelsPerTileY': '512', 'numVoxelsPerTileX': '512', 'dxgiFormat': 'R32_UInt', 'numTilesX': '2', 'numTilesY': '2', 'numTilesZ': '20', 'fileExtension': 'hdf5', 'numTilesW': '2', 'numVoxelsZ': '20', 'numVoxelsY': '1024', 'isSigned': 'false'}
    self.__info = None

    # this is required to connect the deepzoom protocol to mojo zoom
    self.__max_deepzoom_level = 0.0
    self.__max_mojozoom_level = 0.0

    # Actual z-stack and max 3D z-stack
    self.__max_z_tiles = 0
    self.__zSample_max = 80

    self.__has_colormap = False
    self.__colormap = None
    self.__database = None

    self.__volume = None

    # file system regex
    self.__info_regex = re.compile('.*tiledVolumeDescription.xml$')
    self.__colormap_file_regex = re.compile('.*colorMap.hdf5')
    self.__segmentinfo_file_regex = re.compile('.*segmentInfo.db$')

    # handler regex
    self.__query_toc_regex = re.compile('^/' + self.__query + '/contents$')
    self.__query_tilesource_regex = re.compile('^/' + self.__query + '/\d+/$')
    self.__query_tile_regex = re.compile('^/' + self.__query + '/\d+/\d+/\d+_\d+.' + self.__output_format + '$')
    self.__query_volume_regex = re.compile('^/' + self.__query + '/volume/\d+/&.RZ$')
    self.__query_colormap_regex = re.compile('^/' + self.__query + '/colormap$')
    self.__query_segmentinfo_regex = re.compile('^/' + self.__query + '/segmentinfo$')
    self.__query_id_tile_index_regex = re.compile('^/' + self.__query + '/id_tile_index/\d+$')

    self.__setup()

  def get_info(self):

    return self.__info


  def get_input_format(self):

    return self.__input_format


  def get_max_zoomlevel(self):

    return self.__max_mojozoom_level


  def __setup(self):

    # parse the mojo directory
    root = os.path.join(self.__mojo_dir, self.__sub_dir)
    files = os.listdir(root)

    for f in files:


      f_with_dir = os.path.join(root, f)                  ###########
      uf_with_dir = f_with_dir.replace(os.sep, '/')      ###########
      
      # info file
      if self.__info_regex.match(uf_with_dir):
        tree = ET.parse(f_with_dir)
        xml_root = tree.getroot()
        self.__info = xml_root.attrib
        # set the max deepzoom zoom level
        self.__max_deepzoom_level = int(math.log(int(self.__info['numVoxelsX']), 2))
        # set the max mojo zoom level
        self.__max_mojozoom_level = int(math.ceil( math.log(float(self.__info['numVoxelsPerTileX'])/float(self.__info['numVoxelsX']), 0.5) ))
        # get the max number of Z tiles
        self.__max_z_tiles = int(self.__info['numTilesZ'])
        # get the file format
        self.__input_format = str(self.__info['fileExtension'])
        # width and height
        self._width = int(self.__info['numVoxelsX'])
        self._height = int(self.__info['numVoxelsY'])
        self._xtiles = int(self.__info['numTilesX'])
        self._ytiles = int(self.__info['numTilesY'])
        self._voxPerTileX = int(self.__info['numVoxelsPerTileX'])
        self._voxPerTileY = int(self.__info['numVoxelsPerTileY'])

      # colormap
      elif self.__colormap_file_regex.match(f_with_dir):
        hdf5_file = h5py.File(f_with_dir, 'r')
        list_of_names = []
        hdf5_file.visit(list_of_names.append) 
        self.__has_colormap = True
        self.__colormap = hdf5_file[list_of_names[0]].value
        #print('This is a check of color data in datasource.py line 120')
        #print(list_of_names[0])
        #print(self.__colormap)

      # segmentinfo database
      elif self.__segmentinfo_file_regex.match(f_with_dir):

        old_db_file = os.path.join(root,f)
        # new_db_file = old_db_file.replace(self.__mojo_dir, self.__out_dir+'/')
        
        # os.mkdir(self.__out_dir+'/ids')
        # print 'Copied DB from', old_db_file, 'to', new_db_file
        # shutil.copy(old_db_file, new_db_file)
        print('Connecting to DB')
        self.__database = Database(old_db_file)
        # grab existing merge table
        self.__database._merge_table = self.__database.get_merge_table()
        self.__database._lock_table = self.__database.get_lock_table()



  def reconfigure(self):

    self.__setup()

  def get_info_xml(self):

    xml_info = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_info += '<Image xmlns="http://schemas.microsoft.com/deepzoom/2008" TileSize="'+self.__info['numVoxelsPerTileX']+'" Overlap="0" Format="'+self.__output_format+'"><Size Width="'+self.__info['numVoxelsX']+'" Height="'+self.__info['numVoxelsY']+'"/></Image>'

    return xml_info

  def get_tile(self, file):

    pass

  def get_database(self):

    return self.__database

  def get_volume(self, zoomlevel):


    w_path = os.path.join(self.__mojo_dir, self.__sub_dir, 'tiles', 'w='+str(zoomlevel).zfill(8))
    w_path_tmp = os.path.join(self.__mojo_tmp_dir, self.__sub_dir, 'tiles', 'w='+str(zoomlevel).zfill(8))

    dirs = sorted(os.listdir(w_path))

    tile_files = []

    for d in dirs:
      if d.startswith('.'):
        continue

      files = os.listdir(os.path.join(w_path,d))

      for f in files:

        if f.startswith('.'):
          continue

        # check if we have an updated version for this tile
        if os.path.exists(os.path.join(w_path_tmp, d, f)):
          tile_files.append(os.path.join(w_path_tmp, d, f))
        else:
          tile_files.append(os.path.join(w_path, d, f))

    return tile_files

  def handle(self, request):
    '''
    React to a HTTP request.
    '''
    content_type = 'text/html'
    content = None

    # table of contents
    if self.__query_toc_regex.match(request.uri):
      content = {}
      content['zSample_max'] = self.__zSample_max
      content['max_z_tiles'] = self.__max_z_tiles
      content['colormap'] = str(self.__has_colormap).lower()
      content['width'] = self.__info['numVoxelsX']
      content['height'] = self.__info['numVoxelsY']
      content['zoomlevel_count'] = self.__info['numTilesW']

      content = json.dumps(content)

    # tile
    elif self.__query_tile_regex.match(request.uri):

      request_splitted = request.uri.split('/')
      tile_x_y = request_splitted[-1].split('.')[0]
      tile_x, tile_y = tile_x_y.split('_')

      zoomlevel = int(request_splitted[-2])
      slice_number = request_splitted[-3]

      updated_tile_file = os.path.join(self.__mojo_tmp_dir, self.__sub_dir, 'tiles', 'w='+str(zoomlevel).zfill(8), 'z='+slice_number.zfill(8), 'y='+tile_y.zfill(8)+','+'x='+tile_x.zfill(8)+'.'+self.__input_format)
      # print(updated_tile_file)

      if os.path.exists(updated_tile_file):

        content, content_type = self.get_tile(updated_tile_file)
        return content, content_type

      tile_file = os.path.join(self.__mojo_dir, self.__sub_dir, 'tiles', 'w='+str(zoomlevel).zfill(8), 'z='+slice_number.zfill(8), 'y='+tile_y.zfill(8)+','+'x='+tile_x.zfill(8)+'.'+self.__input_format)
      # print(tile_file)

      if os.path.exists(tile_file):

        content, content_type = self.get_tile(tile_file)

    # volume
    elif self.__query_volume_regex.match(request.uri):

      request_splitted = request.uri.split('/')
      zoomlevel = int(request_splitted[-2])

      content, content_type = self.get_volume(zoomlevel)

    # # tile source info
    # elif self.__query_tilesource_regex.match(request.uri):
    #   content = self.get_info_xml()
    #
    # # segment info
    # elif self.__query_segmentinfo_regex.match(request.uri):
    #   content = json.dumps(self.__database.get_segment_info())
    #
    # # tile index
    # elif self.__query_id_tile_index_regex.match(request.uri):
    #   request_splitted = request.uri.split('/')
    #   tile_id = request_splitted[-1]
    #   content = json.dumps(self.__database.get_id_tile_index(tile_id))

    # Only colormap for segmentation
    elif self.__has_colormap and self.__query_colormap_regex.match(request.uri):
      content = json.dumps(self.__colormap.tolist())

    return content, content_type


