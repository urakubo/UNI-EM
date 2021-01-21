###
###
###
import sys, os, time, errno
import glob
import cv2
import numpy as np
from os import path, pardir
import shutil

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))
from system.Params import Params
import miscellaneous.Miscellaneous as m


class DojoExe():

    def _Run(self, parent, params, comm_title):

        print(comm_title,' is running ...')
        tmp_info = Params()
        tmp_info.SetUserInfoAnnotator(params['Dojo Folder'])


        parent.parent.ExecuteCloseFileFolder(params['Empty Folder for Annotator'])
        parent.parent.OpenFolder(params['Empty Folder for Annotator'])
        print('')
        print('Annotator folder created.')
        print('')
        return True



