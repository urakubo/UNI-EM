from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main


class Viewer(object):

  def __init__(self):
    '''
    '''
    self.__query_viewer_regex = re.compile('^/dojo/.*$')


    if getattr(sys, 'frozen', False):
      print('Run on pyinstaller.')
      self.__web_dir = os.path.join(main_dir, "../..", "_web/")
    else:
      print('Run on live python.')
      self.__web_dir = os.path.join(main_dir, "_web/")


  def content_type(self, extension):
    '''
    '''
    return {
      '.js': 'text/javascript',
      '.html': 'text/html',
      '.png': 'image/png',
      '.map': 'text/html',
      '.css': 'text/css',
      '.cur': 'image/x-win-bitmap',
      '.stl': 'image/stl'
    }[extension]

  def handle(self, request):
    '''
    '''

    if not self.__query_viewer_regex.match(request.uri):
      # this is not a valid request for the viewer
      return None, None

    url = request.uri

    # remove query
    url = url.split('?')[0]

    # check if a request goes straight to a folder
    if url.split('/')[-1] == '':
      # add index.html
      url += 'index.html'

    # get filename from query
    requested_file = self.__web_dir + url.replace('/dojo/', '')
    requested_file = os.path.normpath( requested_file )
    extension = os.path.splitext(requested_file)[1]


    # print('requested_file: ', requested_file)
    # print('extension: ', extension)

    if not os.path.exists(requested_file):
      return 'Error 404', 'text/html'


    #if sys.version_info.major == 2:
    #  with open(requested_file, 'r') as f:
    #    content = f.read()
    # else :

    with open(requested_file, 'r', encoding="utf-8_sig") as f:
      content = f.read()

    return content, self.content_type(extension)


