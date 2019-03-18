from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re

class Setup(object):

  def __init__(self,logic,mojo_dir, tmp_dir):
    '''
    '''

    self.__logic = logic

    self.__mojo_dir = mojo_dir
    self.__tmp_dir = tmp_dir

    self.__query_viewer_regex = re.compile('^/dojo/.*$')
    self.__post_data_regex = re.compile('^/setup/data$')

    self.__web_dir = '_web/'

  def content_type(self, extension):
    '''
    '''
    return {
      '.js': 'text/javascript',
      '.html': 'text/html',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.gif': 'image/gif',
      '.map': 'text/html',
      '.css': 'text/css',
      '.stl': 'image/stl',
      '.cur': 'image/x-win-bitmap'
    }[extension]

  def handle(self, request):
    '''
    '''
#    if self.__post_data_regex.match(request.uri):
#      self.setup_data(request)
#      return "OK", 'text/html'

    if not self.__query_viewer_regex.match(request.uri):
      # this is not a valid request for the viewer
      return None, None

    url = request.uri

    # remove query
    url = url.split('?')[0]

    # check if a request goes straight to a folder
#    if url.split('/')[-1] == '':
      # add index.html
#      url += 'setup.html'

    # get filename from query
    requested_file = self.__web_dir + url.replace('/dojo/', '')
    extension = os.path.splitext(requested_file)[1]



    if not os.path.exists(requested_file):
      return 'Error 404', 'text/html'

    with open(requested_file, 'r') as f:
      content = f.read()

    return content, self.content_type(extension)


