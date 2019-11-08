###
###
###


import sys, os, time, errno
import threading
import sqlite3
import json
from marching_cubes import march
from stl import mesh
from os import path, pardir

##

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(path.join(main_dir, "annotator"))
sys.path.append(os.path.join(main_dir, "system"))
sys.path.append(os.path.join(main_dir, "dojoio"))

from Annotator.AnnotatorServer import AnnotatorServerLogic
from DB import DB
from Params import Params
import miscellaneous.Miscellaneous as m
##
###
###
class ControlAnnotatorServer:

    ###
    def __init__(self, u_info):

        ## User info
        self.u_info = u_info

        ## Makedir
        if os.path.isdir(self.u_info.data_annotator_path) == False:
        	os.makedirs(self.u_info.data_annotator_path)

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
        with open(os.path.join(self.u_info.data_annotator_path,"segmentInfo.json"), 'w') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)


    def StartThreadAnnotatorServer(self):
        logic = AnnotatorServerLogic(self.u_info)
        logic.run()

    def LaunchAnnotator(self):
        # self.u_info.worker_loop_stl = asyncio.new_event_loop()
        self.u_info.stl_thread = threading.Thread(target=self.StartThreadAnnotatorServer)
        self.u_info.stl_thread.setDaemon(True) # Stops if control-C
        self.u_info.stl_thread.start()

    def TerminateAnnotator(self):
        print('TerminateAnnotator')
        if self.u_info.stl_thread == None:
            print("3D Annotator is not open\n")
            return False

        print("Asked tornado to exit\n")
        #self.u_info.worker_loop_stl.stop()
        #time.sleep(1)
        #self.u_info.worker_loop_stl.close()
        self.u_info.stl_thread = None
