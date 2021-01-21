###
###
###
import sys, os, time, errno
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
#sys.path.append(path.join(main_dir, "segment"))
#sys.path.append(path.join(main_dir, "system"))
from annotator.CreateAnnotatorFolder.DojoExe import DojoExe

class DojoTab(DojoExe):

    def __init__(self, u_info):

        self.xpitch = 0.006 ## n um
        self.ypitch = 0.006 ## n um
        self.zpitch = 0.03  ## n um
        min_pitch   = 0.001
        max_pitch   = 1.0
        num_digits  = 3

        self.xsampling = 2 ## integer
        self.ysampling = 2 ## integer
        self.zsampling = 1 ## integer
        min_sampling   = 1
        max_sampling   = 16
		

        self.paramfile =  os.path.join( u_info.parameters_path, "CreateAnnot_Hdf5Tab.pickle")

        self.title = 'Dojo'

        self.tips = [
                        'Segmented labels',
                        'Path to empty folder to store Annotator files',
                        'In-slice width in um',
                        'In-slice height in um',
                        'Slice thickness in um',
                        'Downsampling by integer factor',
                        'Downsampling by integer factor',
                        'Downsampling by integer factor'
                        ]

        self.args = [
                        ['Dojo Folder',    'SelectDojoFolder', 'OpenDojoFolder'],
                        ['Empty Folder for Annotator',  'SelectEmptyFolder', 'OpenEmptyFolder'],
                        ['Pitch in X (um)', 'LineEdit_number', [ min_pitch, self.xpitch, max_pitch, num_digits]],
                        ['Pitch in Y (um)', 'LineEdit_number', [ min_pitch, self.ypitch, max_pitch, num_digits]],
                        ['Pitch in Z (um)', 'LineEdit_number', [ min_pitch, self.zpitch, max_pitch, num_digits]],
                        ['Downsampling factor in X','SpinBox',[min_sampling,self.xsampling,max_sampling]],
                        ['Downsampling factor in Y','SpinBox',[min_sampling,self.ysampling,max_sampling]],
                        ['Downsampling factor in Z','SpinBox',[min_sampling,self.zsampling,max_sampling]],
                        ]



