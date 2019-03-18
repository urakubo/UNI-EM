###
###
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, os, time, errno
import threading
import asyncio
import time

import h5py
import numpy as np
import copy
import sqlite3
import json
import lxml
import lxml.etree
from itertools import chain, product
from skimage import measure
from distutils.dir_util import copy_tree
import pickle

import time
import csv
##

from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
plugins_dir = path.join(main_dir, "annotator")
sys.path.append(plugins_dir)
sys.path.append(main_dir)
from StlServer import StlServerLogic
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))

from marching_cubes import march
from stl import mesh

from DB import DB
from Params import Params
import Miscellaneous as m
##
import time
#from pyqtgraph.opengl import GLViewWidget, MeshData
#from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem
#from PyQt4.QtGui import QApplication

if getattr(sys, 'frozen', False):
    stldata_dir = os.path.normpath(os.path.join(main_dir, "../..", "data", "stlviewer"))
else:
    stldata_dir = os.path.normpath(os.path.join(main_dir, "data", "stlviewer"))

if os.path.isdir(stldata_dir) == False:
    os.makedirs(stldata_dir)
###
###
class ControlStlServer:

    ###
    def __init__(self, u_info):

        ## User info
        self.u_info = u_info

        ## Load color file
        colordata = m.load_hdf5(self.u_info.color_map_file, self.u_info.hdf_color_name)
        colnum = colordata.shape[0];


        ## Load database file
        query = "select * from segmentInfo;"
        con = sqlite3.connect( self.u_info.segment_info_db_file )
        cur = con.cursor()
        cur.execute( query ) # Obtain max id
        #data = cur.fetchone()
        data = cur.fetchall()
        con.close()

        keys = ['id', 'name', 'size', 'confidence']
        data_dict = [dict(zip(keys, valuerecord)) for valuerecord in data]


        for i, datum_dict in enumerate(data_dict):
            id  = datum_dict['id']
            if id >= colnum:
                col = {'r': 128, 'g': 128, 'b': 128, 'act': 0}
            else:
                col = {'r': int(colordata[id][0]), 'g': int(colordata[id][1]),  'b': int(colordata[id][2]),  'act': 0}
            data_dict[i].update(col)

        ##
        ## Save
        ##
        with open(os.path.join(stldata_dir,"segmentInfo.json"), 'w') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)


    def StartThreadStlServer(self):
        logic = StlServerLogic(self.u_info)
        logic.run()

    def LaunchStlViewer(self):
        self.u_info.worker_loop_stl = asyncio.new_event_loop()
        self.u_info.stl_thread = threading.Thread(target=self.StartThreadStlServer)
        self.u_info.stl_thread.setDaemon(True) # Stops if control-C
        self.u_info.stl_thread.start()

    def TerminateStlViewer(self):
        print('TerminateStlViewer')
        if self.u_info.stl_thread == None:
            print("3D Annotator is not open\n")
            return False

        print("Asked tornado to exit\n")
        self.u_info.worker_loop_stl.stop()
        time.sleep(1)
        self.u_info.worker_loop_stl.close()
        self.u_info.stl_thread = None
