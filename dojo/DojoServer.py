#!/usr/bin/env python

#
# DOJO Image Server
#

import json
import os
import socket
import sys
import tempfile
import signal

import tornado
import tornado.websocket
import tornado.httpserver
from threading import Thread
import asyncio

from controller 	import Controller
from database 		import Database
from datasource 	import Datasource
from image 			import Image
from segmentation 	import Segmentation
from setup 			import Setup
from viewer 		import Viewer
from websockets 	import Websockets


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")

sys.path.append(os.path.join(main_dir, "system"))
from Params import Params
# import SaveChanges


if getattr(sys, 'frozen', False):
  # Pyinstaller
  path_gfx = os.path.normpath(os.path.join(main_dir, "../..", "_web/gfx"))
else:
  # Live Python
  path_gfx = os.path.join(main_dir, "_web/gfx")


#def doSaneThing(sig, func=None):
#    print "Here I am"
#    raise KeyboardInterrupt
#win32api.SetConsoleCtrlHandler(doSaneThing, 1)


#
# default handler
#
class DojoHandler(tornado.web.RequestHandler):

  def initialize(self, logic):
    self.__logic = logic
  # @tornado.web.asynchronous
  # @tornado.gen.coroutine
  def get(self, uri):
    self.__logic.handle(self)
  # @tornado.web.asynchronous
  # @tornado.gen.coroutine
  def post(self, uri):
    self.__logic.handle(self)

class ServerLogic:

  def func(self, loop):
    loop.stop()

  def __init__( self ):

    pass


  def run( self, u_info ):

    # self, mojo_dir, tmp_dir, /// out_dir, dojoserver

    # register two data sources
    self.__segmentation = Segmentation( u_info.files_path , u_info.tmpdir, self)
    self.__image = Image( u_info.files_path , u_info.tmpdir)

    # and the controller
    self.__controller = Controller( u_info, self.__segmentation.get_database(), self ) ####

    # and the viewer
    self.__viewer = Viewer()



    # and the controller
    if self.__segmentation:
      db = self.__segmentation.get_database()
    else:
      db = None
    self.__controller = Controller( u_info, db, self )



    # and the setup
    self.__setup = Setup(self, u_info.files_path, u_info.tmpdir)

    print('path_gfx: ',path_gfx)
    # running live

    ####
    ev_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ev_loop)

    dojo = tornado.web.Application([
      (r'/dojo/gfx/(.*)', tornado.web.StaticFileHandler, {'path': path_gfx}),
      (r'/ws', Websockets, dict(controller=self.__controller)),
      (r'/(.*)', DojoHandler, dict(logic=self))
    ],debug=True,autoreload=True) #            (r'/dojo/gfx/(.*)', tornado.web.StaticFileHandler, {'path': '/dojo/gfx'})


    # dojo.listen(u_info.port, max_buffer_size=1024*1024*150000)
    server = tornado.httpserver.HTTPServer(dojo)
    server.listen(u_info.port)

    print('*'*80)
    print('*', 'DOJO RUNNING')
    print('*')
    print('*', 'open', '[ http://' + u_info.ip + ':' + str(u_info.port) + '/dojo/ ] ')
    print('*'*80)

    tornado.ioloop.IOLoop.instance().start()
    ev_loop.stop()
    ev_loop.close()
    server.stop()

    # def sig_handler(signum, frame):
    #  IOLoop.current().add_callback_from_signal(receiver.shutdown)

    print("Tornado web server stops.")

    return

    ##
    ## IOLoop.instance().stop()
    ## return
    ##

  def stop():
    asyncio.asyncio_loop.stop()
    server.stop()
    # thread.join()

  def get_image(self):
    return self.__image


  def get_segmentation(self):
    return self.__segmentation


  def get_controller(self):
    return self.__controller


  def handle( self, r ):

    content = None

    # the access to the viewer
    #if not self.__configured:
    #  content, content_type = self.__setup.handle(r.request)
    #else:
    # viewer is ready
    content, content_type = self.__viewer.handle(r.request)

    # let the data sources handle the request
    if not content:
      content, content_type = self.__segmentation.handle(r.request)

    if not content:
      content, content_type = self.__image.handle(r.request)

    # invalid request
    if not content:
      content = 'Error 404'
      content_type = 'text/html'

    # print 'IP',r.request.remote_ip

    r.set_header('Access-Control-Allow-Origin', '*')
    r.set_header('Content-Type', content_type)
    r.write(content)


  def close(self, signal, frame):
    print('Sayonara..!!')
    output = {}
    output['origin'] = 'SERVER'

    sys.exit(0)

