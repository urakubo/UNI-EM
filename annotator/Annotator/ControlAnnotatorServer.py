###
###
###


import sys, os, time, errno
import threading
from os import path, pardir

##

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(path.join(main_dir, "annotator"))
sys.path.append(os.path.join(main_dir, "system"))

from Annotator.AnnotatorServer import AnnotatorServerLogic
from Params import Params
import miscellaneous.Miscellaneous as m
##
##
##
class ControlAnnotatorServer:

    def __init__(self, parent):
        self.u_info = parent.u_info
        self.parent = parent

    def StartThreadAnnotatorServer(self):
        logic = AnnotatorServerLogic(self.u_info)
        logic.run()

    def LaunchAnnotator(self):  # wxGlade: ControlPanel.<event_handler>

		#
        if ( self.u_info.annotator_files_found != True ):
            print("Annotator has not been specified.\n")
            return False

		# Window title
        frame_statusbar_fields = "Annotator: " + self.u_info.annotator_files_path
        self.parent.setWindowTitle(frame_statusbar_fields)
        
        # Unlock Folder
        m.UnlockFolder(self.u_info, self.u_info.annotator_files_path)

        ## Close
        # self.u_info.worker_loop_stl = asyncio.new_event_loop()
        self.u_info.annotator_thread = threading.Thread(target=self.StartThreadAnnotatorServer)
        self.u_info.annotator_thread.setDaemon(True) # Stops if control-C
        self.u_info.annotator_thread.start()
        
        self.parent.table_widget.addTab('annotator', '3D Annotator', self.u_info.url_annotator+'index.html' )

		##
        return True
		##

    def TerminateAnnotator(self):
        print('TerminateAnnotator')
        if self.u_info.annotator_thread == None:
            print("3D Annotator is not open\n")
            return False

        print("Asked tornado to exit\n")
        #self.u_info.worker_loop_stl.stop()
        #time.sleep(1)
        #self.u_info.worker_loop_stl.close()
        self.u_info.annotator_thread = None




