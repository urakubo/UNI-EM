###
###
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, os, time, errno

import socket
import threading
import numpy as np
import copy
#import shutil
import sqlite3
import lxml
import lxml.etree
from itertools import chain, product
from skimage import measure
from distutils.dir_util import copy_tree
import pickle
#import threading
#import subprocess as s

import time
import csv
##

from os import path, pardir


main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
plugins_dir  = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))

from marching_cubes import march
from stl import mesh

from DB import DB
from Params import Params
import Miscellaneous as m
import time
# import tensorflow as tf
# from tensorboard import main as tb

from tensorboard import default
from tensorboard import program
###


###
class Tensorboard:

    ###
    def __init__(self, parent):
        ##
        self.parent = parent
        ## User info
        self.u_info = self.parent.u_info
        ##
        self.u_info.dojo_thread = threading.Thread(target=self.StartThreadTensorboard)
        self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
        self.u_info.dojo_thread.start()
        time.sleep(1)
        ##
        return
        ##
    ###
    def StartThreadTensorboard(self):


        # Remove http messages
        # log = logging.getLogger('werkzeug').setLevel(logging.ERROR)

		# Tensorborad V1.12
        tb = program.TensorBoard(default.get_plugins(), default.get_assets_zip_provider())
        tb.configure(argv=[None, '--logdir', self.u_info.tensorboard_path,'--host', socket.gethostbyname(socket.gethostname())])
        tb.launch()

		# Tensorborad V1.10
        # tb = program.TensorBoard(default.PLUGIN_LOADERS, default.get_assets_zip_provider())
        # tb.configure(argv=['--logdir', tfevents_dir,'--host', socket.gethostbyname(socket.gethostname())])
        #tb.main()


# Check the following we page.
# https://stackoverflow.com/questions/42158694/how-to-run-tensorboard-from-python-scipt-in-virtualenv
