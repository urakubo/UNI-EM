###
###
###
import sys, os, time, errno
from os import path, pardir
import glob
import numpy as np
import json
import sqlite3
import h5py



main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
#sys.path.append(path.join(main_dir, "system"))
import miscellaneous.Miscellaneous as m


class Hdf5Exe():

    def _Run(self, parent, params, comm_title):

        print(comm_title,' is running ...')

        with h5py.File(params['Hdf5 file containing segmentation volume'], 'r') as f:		
            pass

        #comm = parent.u_info
        parent.parent.ExecuteCloseFileFolder(params['Empty Folder for Annotator'])
        parent.parent.OpenFolder(params['Empty Folder for Annotator'])
        print('')
        print('Annotator folder created.')
        print('')
        return True



