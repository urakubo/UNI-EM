#
#
#
import os, sys
import numpy as np
import socket
import tempfile

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main

class Params:
    def __init__(self):

        #
        # Environmental variables
        #
        if os.name == 'nt':
            desktop_path    = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + str(os.sep) + "Desktop"
            mydocument_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + str(os.sep) + "Documents"
            user_path       = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
        else:
            desktop_path = '~/Desktop'
            mydocument_path = '~/Documents'
            user_path = '~'

        user_path = main_dir

        ## Server infos of Dojo and 3D Annotator
        self.ip = socket.gethostbyname(socket.gethostname())
        self.configured = True
        self.port = 8887
        self.dojo_thread = None
        self.tensorboard_thread = None
        self.url  = 'http://' + self.ip + ':' + str(self.port) + '/dojo/'
        self.port_stl = 3000
        self.url_stl  = 'http://' + self.ip + ':' + str(self.port_stl) + '/'
        self.stl_thread = None


        # Mojo unit image size for import
        self.tile_num_pixels_y  = 512
        self.tile_num_pixels_x  = 512
        self.ncolors            = 16000 ########## 65535
        self.tile_path_wz       = str(os.sep) + 'w={0:08d}' + str(os.sep) + 'z={1:08d}'
        self.tile_ids_filename_wzyx = str(os.sep) + 'w={0:08d}' + str(os.sep) + 'z={1:08d}' + str(os.sep) + 'y={2:08d},x={3:08d}.hdf5'
        self.tile_images_filename_wzyx = str(os.sep) + 'w={0:08d}' + str(os.sep) + 'z={1:08d}' + str(os.sep) + 'y={2:08d},x={3:08d}.tif'

        self.tile_ids_filename_yx = 'y={0:08d},x={1:08d}.hdf5'
        self.tile_images_filename_yx = 'y={0:08d},x={1:08d}.tif'

        self.tile_var_name      = 'IdMap'
        # self.dtype_tile         = np.uint32
        self.ids_dtype          = np.uint32
        self.images_dtype       = np.uint8
        self.hdf_color_name = 'idColorMap'

        self.backup_db_name = 'idTileIndex'
        self.image_extension = 'tif'
        self.id_extension    = 'hdf5'

        # Export
        self.export_col_name = 'colormap'
        self.export_db_name = 'segmentInfo'
        self.export_db_ids = ['id', 'name', 'size', 'confidence', 'type', 'subtype']

        # self.export_images_dir          = 'export_images'
        # self.export_ids_dir             = 'export_ids'
        # self.export_images_name         = 'z%08d'
        # self.export_ids_name            = 'z%08d'

        self.fname_menu = 'menu.json'

        # Mojo file paths
        self.files_found = False
        self.files_path  = user_path
        self.flag_undo   = 0
        self.flag_redo   = 0


        ## File system
        self.max_num_recent_files = 8
        self.max_num_open_files   = 20
        self.open_files        = []
        self.open_files4lock   = {}
        self.open_files_type   = {}


        # Data path
        if getattr(sys, 'frozen', False):
            # print('Run on pyinstaller.')
            self.data_path    = os.path.normpath(os.path.join(main_dir, "..","..","data"))
            self.gfx_path     = os.path.normpath(os.path.join(main_dir, "..","..", "_web_dojo","gfx"))
            self.web_path     = os.path.normpath(os.path.join(main_dir, "..","..", "_web_dojo"))
            self.web_annotator_path = os.path.normpath(os.path.join(main_dir, "..","..", "_web_annotator"))
            self.data_annotator_path = os.path.normpath(os.path.join(main_dir, "..","..", "data", "annotator"))
            
            ext_os = lambda prg: f'{prg}.exe' if(os.name == 'nt') else prg
            self.exec_translate 		= [ os.path.join(main_dir, ext_os('translate')) ]
            self.exec_run_inference 	= [ os.path.join(main_dir, ext_os('run_inference_win')) ]
            self.exec_compute_partition = [ os.path.join(main_dir, ext_os('compute_partitions')) ]
            self.exec_build_coordinates = [ os.path.join(main_dir, ext_os('build_coordinates')) ]
            self.exec_train 			= [ os.path.join(main_dir, ext_os('train')) ]
            self.exec_tensorboard 		= [ os.path.join(main_dir, ext_os('launch_tensorboard')) ]
            self.exec_template 			= [ os.path.join(main_dir, ext_os('run_example')) ]

        else:
            # print('Run on live python.')
            self.data_path    = os.path.join(main_dir, "data")
            self.gfx_path     = os.path.join(main_dir, "_web_dojo","gfx")
            self.web_path     = os.path.join(main_dir, "_web_dojo")
            self.web_annotator_path = os.path.normpath(os.path.join(main_dir, "_web_annotator"))
            self.data_annotator_path = os.path.normpath(os.path.join(main_dir, "data", "annotator"))

            _2D_DNN_dir = os.path.join(main_dir, 'segment', '_2D_DNN')
            _3D_FFN_dir = os.path.join(main_dir, 'segment', '_3D_FFN', 'ffn')
            python_exe = sys.executable # 'python', 'python3', etc
            self.exec_translate 	= [python_exe , os.path.join(_2D_DNN_dir, 'translate.py')]
            self.exec_run_inference = [python_exe , os.path.join(_3D_FFN_dir, 'run_inference_win.py')]
            self.exec_compute_partition = [python_exe , os.path.join(_3D_FFN_dir, 'compute_partitions.py')]
            self.exec_build_coordinates = [python_exe , os.path.join(_3D_FFN_dir, 'build_coordinates.py')]
            self.exec_train = [python_exe, os.path.join(_3D_FFN_dir, 'train.py')]
            self.exec_tensorboard = ['tensorboard']
            self.exec_template = [python_exe, os.path.join(main_dir,  'plugins', 'Template', 'run_example.py')]



        self.parameters_path = os.path.normpath( path.join(self.data_path, "parameters") )


    def SetUserInfo(self, user_path):

        #
        # User dependent variables
        #

        self.files_path                = user_path
        self.ids_path                  = os.path.join(self.files_path   ,'ids')
        self.tile_ids_path             = os.path.join(self.ids_path     ,'tiles')
        self.tile_ids_volume_file      = os.path.join(self.ids_path     ,'tiledVolumeDescription.xml')
        self.color_map_file            = os.path.join(self.ids_path     ,'colorMap.hdf5')
        self.segment_info_db_file      = os.path.join(self.ids_path     ,'segmentInfo.db')
        self.segment_info_db_undo_file  = os.path.join(self.ids_path    ,'segmentInfo_undo.pickle')
        self.segment_info_db_redo_file  = os.path.join(self.ids_path    ,'segmentInfo_redo.pickle')

        self.images_path               = os.path.join(self.files_path   ,'images')
        self.tile_images_path          = os.path.join(self.images_path  ,'tiles')
        self.tile_images_volume_file   = os.path.join(self.images_path  ,'tiledVolumeDescription.xml')

        self.ids_files_undo             = []
        self.ids_files_redo             = []
        self.flag_undo                  = 0
        self.flag_redo                  = 0

        self.tmpdir = tempfile.mkdtemp()
        self.merge_table = []
        self.tmp_ids_path = os.path.join(self.tmpdir, 'ids')
        self.tmp_tile_ids_path = os.path.join(self.tmpdir, 'ids', 'tiles')

        ## Recheck current ip
        self.ip = socket.gethostbyname(socket.gethostname())
        self.url  = 'http://' + self.ip + ':' + str(self.port) + '/dojo/'
        self.url_stl  = 'http://' + self.ip + ':' + str(self.port_stl) + '/'
