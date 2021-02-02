###
###
###
import sys, os, time, errno
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
#sys.path.append(path.join(main_dir, "system"))
from annotator.CreateAnnotatorFolder.Hdf5Exe import Hdf5Exe

class Hdf5Tab(Hdf5Exe):

    def __init__(self, u_info):

        self.xpitch = 0.02 ## n um
        self.ypitch = 0.02 ## n um
        self.zpitch = 0.02  ## n um
        min_pitch   = 0.001
        max_pitch   = 1.0
        num_digits  = 3

        self.xsampling = 1 ## integer
        self.ysampling = 1 ## integer
        self.zsampling = 1 ## integer
        min_sampling   = 1
        max_sampling   = 16
		
        default_container_name = 'dendrite'


        self.paramfile =  os.path.join( u_info.parameters_path, "CreateAnnot_Hdf5Tab.pickle")

        self.title = 'Hdf5'

        self.tips = [
                        'HDF5 file containing a segmention volume',
                        'Contaniner name that stores the segmentation volume',
                        'Path to empty folder to store Annotator files',
                        'In-slice width in um',
                        'In-slice height in um',
                        'Slice thickness in um',
                        'Downsampling by integer factor',
                        'Downsampling by integer factor',
                        'Downsampling by integer factor'
                        ]

        self.args = [
                        ['Hdf5 file containing segmentation volume', 'SelectHdf5File', 'OpenHdf5File'],
                        ['Container name', 'LineEdit', default_container_name, None],
                        ['Empty folder for annotator',  'SelectEmptyFolder', 'OpenEmptyFolder'],
                        ['Pitch in X (um)', 'LineEdit_number', [ min_pitch, self.xpitch, max_pitch, num_digits]],
                        ['Pitch in Y (um)', 'LineEdit_number', [ min_pitch, self.ypitch, max_pitch, num_digits]],
                        ['Pitch in Z (um)', 'LineEdit_number', [ min_pitch, self.zpitch, max_pitch, num_digits]],
                        ['Downsampling factor in X','SpinBox',[min_sampling,self.xsampling,max_sampling]],
                        ['Downsampling factor in Y','SpinBox',[min_sampling,self.ysampling,max_sampling]],
                        ['Downsampling factor in Z','SpinBox',[min_sampling,self.zsampling,max_sampling]],
                        ]



