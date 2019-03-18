from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import h5py
import mahotas as mh
import numpy as np
import os
import re
import zlib
#from io import StringIO
from io import BytesIO
from collections import OrderedDict
from datasource import Datasource

class Segmentation(Datasource):

  def __init__(self, mojo_dir, tmp_dir, dojoserver):
    '''
    @override
    '''
    query = 'segmentation'
    input_format = 'hdf5'
    output_format = 'raw'
    sub_dir = 'ids'

    super(Segmentation, self).__init__(mojo_dir, tmp_dir, query, input_format, output_format, sub_dir)

    self.__dojoserver = dojoserver

  def get_volume_data(self):

    files = super(Segmentation, self).get_volume(1)

    out = None
    out_is_there = False

    for i,f in enumerate(files):

      hdf5_file = h5py.File(f)
      list_of_names = []
      hdf5_file.visit(list_of_names.append)
      image_data = hdf5_file[list_of_names[0]].value
      hdf5_file.close()

      if out_is_there:
        out = np.dstack([out, image_data])
      else:
        out = image_data
        out_is_there = True

    print('Loaded volume data', out.shape)

    return out

  def get_volume(self, zoomlevel):
    '''
    @override
    '''
    files = super(Segmentation, self).get_volume(zoomlevel)

    out = None
    out_is_there = False

    # Sample all slices or a maximum number of z slices from all files
    for i in np.linspace(0,len(files)-1, num=min(len(files),self._Datasource__zSample_max)).astype('int'):

      list_of_names = []
      hdf5_file = h5py.File(files[i])
      hdf5_file.visit(list_of_names.append)
      image_data = hdf5_file[list_of_names[0]].value
      hdf5_file.close()

      if out_is_there:
        #out = np.dstack([out, input_image])
        out = np.concatenate([out, image_data.flatten()])
      else:
        #out = input_image
        out = image_data.flatten()
        out_is_there = True

    c_image_data = zlib.compress(out)

    print('Loaded volume', out.shape)

    output = BytesIO()
    output.write(c_image_data)

    content = output.getvalue()
    content_type = 'application/octstream'

    return content, content_type

  def get_tile(self, file):

    super(Segmentation, self).get_tile(file)

    hdf5_file = h5py.File(file)
    list_of_names = []
    hdf5_file.visit(list_of_names.append)
    image_data = hdf5_file[list_of_names[0]].value
    hdf5_file.close()

    #print file, image_data[0][0], image_data.shape
    # print image_data.dtype

    #
    # NEW: WE NOW APPLY THE MERGE TABLE FROM THE DATABASE HERE
    #
    lut = self.__dojoserver.get_controller().get_hard_merge_table()
    # print lut
    hardened_image_data = lut[image_data]
    # print 'hardened', hardened_image_data.shape

    # mh.imsave('/tmp/'+os.path.basename(file)+'.tif', hardened_image_data.astype(np.uint32))
    # print 'TIF saved'

    c_image_data = zlib.compress(hardened_image_data.astype(np.uint32))

    output = BytesIO() # StringIO()
    output.write(c_image_data)

    content = output.getvalue()
    content_type = 'application/octstream'

    # print('Size of seg tile: ', content)

    return content, content_type

  def handle(self, request):
    '''
    @override
    '''
    return super(Segmentation, self).handle(request)
