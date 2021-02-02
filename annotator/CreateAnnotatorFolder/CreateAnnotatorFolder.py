###
###
###
import sys, os, time, errno
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QDialog
from PyQt5.QtGui import QIcon
from os import path, pardir
import h5py
import json
import numpy as np


main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "annotator"))

import miscellaneous.Miscellaneous as m
from system.Params import Params
from miscellaneous.TabGenerator import TabGenerator
from annotator.CreateAnnotatorFolder.ImagesTab  import ImagesTab
from annotator.CreateAnnotatorFolder.Hdf5Tab  import Hdf5Tab
from annotator.CreateAnnotatorFolder.DojoTab  import DojoTab

class GenerateDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 600
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "Create Annotator Folder"
        self.initUI()


    def initUI(self):

        ##
        ## Define tab
        ##
        self.layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.resize(300, 500)
        tab_source = TabGenerator(self)

        ##
        ## Images
        ##
        Images    = ImagesTab(self.u_info)
        tab1      = tab_source.GenerateTabWidget(Images) # Widget
        tabs.addTab(tab1, "png/tiff")

        ##
        ## hdf5
        ##
        hdf5      = Hdf5Tab(self.u_info)
        tab2      = tab_source.GenerateTabWidget(hdf5) # Widget
        tabs.addTab(tab2,"hdf5")

        ##
        ## Dojo
        ##
        Dojo      = DojoTab(self.u_info)
        tab2      = tab_source.GenerateTabWidget(Dojo) # Widget
        tabs.addTab(tab2,"Dojo")

        # Add tabs to widget
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()


#########################


    def SharedPreprocess(self, params, comm_title):

        print('Annotator folder is being generated for', comm_title)
        targ = Params()
        targ.SetUserInfoAnnotator(params['Empty Folder for Annotator'])

        if os.path.isdir(targ.surfaces_path) == False:
        	m.mkdir_safe(targ.surfaces_path)
        	m.mkdir_safe(targ.surfaces_whole_path)
        if os.path.isdir(targ.skeletons_path) == False:
        	m.mkdir_safe(targ.skeletons_path)
        	m.mkdir_safe(targ.skeletons_whole_path)
        if os.path.isdir(targ.volume_path) == False:
        	m.mkdir_safe(targ.volume_path)
        if os.path.isdir(targ.paint_path) == False:
        	m.mkdir_safe(targ.paint_path)

        return targ

    def SharedGenerateInfoFile(self, ids_volume, surfaces_segment_info_json_file):
        ids_nums = np.unique(ids_volume, return_counts=True)
        ids   = ids_nums[0]
        names = [str(id).zfill(10) for id in ids]
        sizes = ids_nums[1]
        colormap = np.random.randint(255, size=(ids.shape[0], 3), dtype='int')

        if ids[0] == 0:
        	ids   = np.delete(ids, 0)
        	names.pop(0)
        	sizes = np.delete(sizes, 0)
        	colormap = np.delete(colormap, 0, 0)

        ids      = ids.tolist()
        sizes    = sizes.tolist()
        colormap = colormap.tolist()

        print('Constainer shape: ', ids_volume.shape)
        print('IDs  : ', ids)
        print('names: ', names)
        print('sizes: ', sizes)
        print('cols : ', colormap)

		##
        keys = ['id', 'name', 'size']
        data_dict = [dict(zip(keys, valuerecord)) for valuerecord in zip(ids, names, sizes)]

        for i in range(len(data_dict)):
        	col = {'confidence': 0, 'r': colormap[i][0], 'g': colormap[i][1],  'b': colormap[i][2],  'act': 0}
        	data_dict[i].update(col)

        print('data_dict: ', data_dict)

        with open( surfaces_segment_info_json_file , 'w') as f:
        	json.dump(data_dict, f, indent=2, ensure_ascii=False)

        return True


    def SharedPostProcess(self, params, targ, ids_volume):
		##
        print("params['Pitch in X (um)']", params['Pitch in X (um)'])
        print("params['Downsampling factor in X']", params['Downsampling factor in X'])
		
        ph = params['Pitch in X (um)']
        pw = params['Pitch in Y (um)']
        pz = params['Pitch in Z (um)']
        ch = int(params['Downsampling factor in X'])
        cw = int(params['Downsampling factor in Y'])
        cz = int(params['Downsampling factor in Z'])
        ph *= ch
        pw *= cw
        pz *= cz
        wmax = ids_volume.shape[0]
        hmax = ids_volume.shape[1]
        zmax = ids_volume.shape[2]
		##
        with h5py.File(targ.volume_file, 'w') as f:		
        	f.create_dataset('volume', data=ids_volume)
		##
        data_dict = {
		    	'boundingbox_voxel':{
		    		'x': hmax,
		    		'y': wmax,
		    		'z': zmax
		    		},
		    	'boundingbox_um':{
		    		'x': ph * hmax,
		    		'y': pw * wmax,
		    		'z': pz * zmax
		    		},
		    	'pitch_um':{
		    		'x': ph,
		    		'y': pw,
		    		'z': pz
		    		},
				}
        with open( targ.surfaces_volume_description_json_file , 'w') as f:
        	json.dump(data_dict, f, indent=2, ensure_ascii=False)

        self.parent.ExecuteCloseFileFolder(params['Empty folder for annotator'])
        self.parent.OpenFolder(params['Empty folder for annotator'])
        print('')
        print('Annotator folder created.')
        print('')

        return True

