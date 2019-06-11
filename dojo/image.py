
import os
import re
from io import BytesIO
from datasource import Datasource
import numpy as np
import zlib
import cv2



class Image(Datasource):

  def __init__(self, mojo_dir, tmp_dir):
    '''
    @override
    '''
    query = 'image'
    input_format = None # input_format = None 180905
    output_format = 'jpg'
    sub_dir = 'images'

    super(Image, self).__init__(mojo_dir, tmp_dir, query, input_format, output_format, sub_dir)

  def get_volume(self, zoomlevel):
    '''
    @override
    '''
    files = super(Image, self).get_volume(zoomlevel)

    out = None
    out_is_there = False

    # Sample all slices or a maximum number of z slices from all files
    for i in np.linspace(0,len(files)-1, num=min(len(files),self._Datasource__zSample_max)).astype('int'):

      print(files[i])   ##################################################
      input_image = cv2.imread(files[i])

      if out_is_there:
        #out = np.dstack([out, input_image])
        out = np.concatenate([out, input_image.flatten()])
      else:
        #out = input_image
        out = input_image.flatten()
        out_is_there = True

    c_image_data = zlib.compress(out)

    output = BytesIO()
    output.write(c_image_data)

    content = output.getvalue()
    content_type = 'application/octstream'

    return content, content_type

  def get_tile(self, file):
    '''
    @override
    '''
    super(Image, self).get_tile(file)

    image_data = cv2.imread(file,1)
    #if image_data.mode != "RGB":	#####
    #    image_data = image_data.convert("RGB") #####


    content = cv2.imencode('.jpg', image_data, [cv2.IMWRITE_JPEG_QUALITY, 90])[1].tostring()

    content_type = 'image/jpeg'

    return content, content_type

  def handle(self, request):
    '''
    @override
    '''
    return super(Image, self).handle(request)



