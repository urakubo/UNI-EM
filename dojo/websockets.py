from controller import Controller

import struct
######
try:
    import SocketServer
except ImportError:
    import socketserver
######
from base64 import b64encode
from hashlib import sha1
#from mimetools import Message
import tornado
import tornado.websocket

cl = []

class Websockets(tornado.websocket.WebSocketHandler):

  def initialize(self, controller):
    '''
    '''
    self.__controller = controller

  def open(self):
    '''
    '''
    if self not in cl:
      cl.append(self)

    self.__controller.handshake(self)

  def on_close(self):
    '''
    '''
    if self in cl:
      cl.remove(self)

  def on_message(self, message):
    '''
    '''
    self.__controller.on_message(message)

  def send(self, message):
    '''
    '''
    for c in cl:
      c.write_message(message)

