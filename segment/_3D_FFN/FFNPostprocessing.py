###
###
###
import sys, os, time, errno
import numpy as np
# import copy
# from itertools import chain
# import subprocess as s
# import threading
import miscellaneous.Miscellaneous as m


from PyQt5.QtWidgets import QMessageBox

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "system"))

class FFNPostprocessing():


    def _Run(self, parent, params, comm_title):
        ##
        print('Start postprocesing.')
        print(params['Output Filetype'])

        data = np.load(params['Target Sementation File (npz)'])
        print('File contents :', data.files)
        segmentation = data['segmentation']
        print('Segmentation image size: ', segmentation.shape)
        filetype = params['Output Filetype']
        ##
        ##
        if (filetype == '8-bit color PNG') or (filetype == '8-bit color TIFF'):
            ids = np.max(segmentation)
            print('Max segmentation ID: ', ids)
            colormap = np.random.randint(255, size=(ids+2, 3), dtype=np.uint64)
            colormap[0,:] = 0
        ##
        m.UnlockFolder(parent.u_info, params['Output Segmentation Folder'])
        ##
        for idz in range(segmentation.shape[0]):
            image2d = segmentation[idz, :, :]
            print('image2d size: ', image2d.shape)

            if filetype == '16-bit gray scale TIFF':
                filename = os.path.join(params['Output Segmentation Folder'], 'z{:0=4}.tif'.format(idz))
                m.save_tif16(image2d, filename)
            elif filetype == '8-bit gray scale TIFF':
                filename = os.path.join(params['Output Segmentation Folder'], 'z{:0=4}.tif'.format(idz))
                m.save_tif8(image2d, filename)
            elif filetype == '16-bit gray scale PNG':
                filename = os.path.join(params['Output Segmentation Folder'], 'z{:0=4}.png'.format(idz))
                m.save_png16(image2d, filename)
            elif filetype == '8-bit gray scale PNG':
                filename = os.path.join(params['Output Segmentation Folder'], 'z{:0=4}.png'.format(idz))
                m.save_png8(image2d, filename)
            elif filetype == '8-bit color PNG' :
                filename = os.path.join(params['Output Segmentation Folder'], 'z{:0=4}.png'.format(idz))
                m.save_pngc(image2d, filename, colormap)
            elif filetype == '8-bit color TIFF' :
                filename = os.path.join(params['Output Segmentation Folder'], 'z{:0=4}.tif'.format(idz))
                m.save_tifc(image2d, filename, colormap)
            else:
                print('Data was not saved.')
        ##
        print(comm_title, 'was finished.')
        flag = m.LockFolder(parent.u_info, params['Output Segmentation Folder'])
        return flag
        ##

    def __init__(self, u_info):
        ##
        datadir = u_info.data_path

        target_inference_file = os.path.join(datadir, "ffn","0", "0", "seg-0_0_0.npz")

        self.paramfile = os.path.join(u_info.parameters_path, "FFN_Postprocessing.pickle")

        self.title = 'Postprocessing'

        self.tips = [
                        'Input: Path to folder containing an inference file',
                        'Output segmentation folder'
                        'Output filetype'
                        ]

        self.args = [
                        ['Target Sementation File (npz)',  'LineEdit', target_inference_file, 'BrowseFile'],
                        ['Output Segmentation Folder',   'SelectImageFolder', 'OpenImageFolder'],
                        ['Output Filetype', 'ComboBox', ["8-bit color PNG", "16-bit gray scale PNG", "8-bit gray scale PNG", 
                                                         "8-bit color TIFF", "16-bit gray scale TIFF", "8-bit gray scale TIFF"]],
            ]



