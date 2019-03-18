#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import h5py
import lxml
import lxml.etree
from itertools import chain
import shutil

from DB import DB
from Params import Params
import Miscellaneous as m

def Undo( u_info ):
    if u_info.flag_undo < 1 :
        print('No undo buffer.')
        return False

    u_info.flag_undo = 0
    ## Load DB
    db = DB(u_info)

    ##
    print('Undo: Database updated.')
    db.Backup( u_info.segment_info_db_redo_file )
    db.Restore( u_info.segment_info_db_undo_file )
    print('Undo: Id panels updated.')
    u_info.ids_files_redo = u_info.ids_files_undo
    u_info.ids_files_undo = []
    for filename in u_info.ids_files_undo:
        shutil.move(filename, filename+'~')      ## Backup for redo
        shutil.move(filename + '_', filename )   ## Copy from undo backup

    u_info.flag_redo      = 1
    print('Undo: Completed.')


def Redo( u_info ):
    if u_info.flag_redo < 1 :
        print('No redo buffer.')
        return False

    u_info.flag_redo      = 0
    ## Load DB
    db = DB(u_info)

    ##
    print('Redo: Database updated.')
    db.Backup( u_info.segment_info_db_undo_file )
    db.restore( u_info.segment_info_db_redo_file )
    print('Redo: Id panels updated.')
    u_info.ids_files_undo = u_info.ids_files_redo
    u_info.ids_files_redo = []
    for filename in u_info.ids_files_redo:
        shutil.move(filename, filename+'_')      ## Backup for undo
        shutil.move(filename + '~', filename )   ## Copy from redo backup
    u_info.flag_undo      = 1
    print('Redo: Completed.')


