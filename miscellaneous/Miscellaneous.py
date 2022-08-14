##
##
##

import os, sys
import numpy as np
import h5py
import PIL
import PIL.Image
import cv2
import png
import tifffile
from itertools import product
import glob
import math

from PyQt5.QtWidgets import QDialog, QDialogButtonBox,\
    QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QVBoxLayout, \
    QTreeView, QFileSystemModel, QListView, QTableView, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot,  QAbstractListModel, QModelIndex, QVariant, QDir, QSize


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir = path.join(main_dir, "icons")
sys.path.append(main_dir)
# sys.path.append(os.path.join(main_dir, "segment"))
# sys.path.append(os.path.join(main_dir, "filesystem"))

# import miscellaneous.Miscellaneous as m



def assign_regions_for_merge(im_size, split_size, overlap_size):
	overlap_size_2 = overlap_size // 2
	unit_size = split_size - overlap_size
	num       = math.ceil( (im_size - overlap_size) / unit_size )
	
	if   num == 1:
		panels = [[0, im_size]]
		merged = [[0, im_size]]
		return panels, merged
	elif num == 2:
		panels = [ [0, split_size - overlap_size_2], [overlap_size_2, im_size - split_size] ]
		merged = [ [0, unit_size + overlap_size_2], [unit_size + overlap_size_2, im_size] ]
		return panels, merged
	elif num >= 3:
		panels = [ [0, split_size - overlap_size_2] ]
		merged = [ [0, split_size - overlap_size_2] ]
		for i in  range( 1, num ):
			m0 = i * unit_size + overlap_size_2
			m1 = (i+1) * unit_size + overlap_size_2
			p0 = overlap_size_2
			p1 = unit_size + overlap_size_2
			if im_size < m1:
				m1 = im_size
				p1 = np.mod(im_size, unit_size) # -1
			merged.append([m0, m1])
			panels.append([p0, p1])
		return panels, merged

def crop_with_overlap(im_size, split_size, overlap_size):
	unit_size = split_size - overlap_size
	num       = math.ceil( (im_size - overlap_size) / unit_size )
	ws = []
	for i in  range( num ):
		w0 = i * unit_size
		w1 = (i+1) * unit_size + overlap_size
		w1 = min([w1, im_size])
		ws.append([w0, w1])
	return ws, num


def obtain_list_image_files( image_folder ):
	types = ['jpg', 'png', 'tif', 'tiff']
	input_files = []
	for ext in types:
		paths = os.path.join( image_folder , '*.{}'.format(ext))
		input_files.extend(glob.glob(paths))
	input_files = sorted(input_files)
	if len(input_files) == 0:
		print('No images in the Image Folder.')
		return False

	return input_files


def ObtainImageFiles(input_path):
    search1 = os.path.join(input_path, '*.png')
    search2 = os.path.join(input_path, '*.tif')
    search3 = os.path.join(input_path, '*.tiff')
    filestack = sorted(glob.glob(search1))
    filestack.extend(sorted(glob.glob(search2)))
    filestack.extend(sorted(glob.glob(search3)))
    return filestack


def read_image(input_file, ext):
	#root, ext = os.path.splitext(os.path.basename(input_file))
	if ext in ['tif', 'tiff'] :
		im = imread(input_file)
	else :
		im = imread(input_file, cv2.IMREAD_UNCHANGED)
	return im


def read_seg_image(input_file, ext):
	#ext = os.path.splitext(os.path.basename(input_file))[1][1:]
	if ext in ['tif', 'tiff'] :
		im = imread(input_file)
	else :
		im = imread(input_file, cv2.IMREAD_UNCHANGED)
	if im.ndim == 3 and im.shape[2] == 3:
		im = im[:,:,0].astype(int) \
			+ im[:,:,1].astype(int)*256 \
			+ im[:,:,2].astype(int)*256*256

	elif im.ndim == 3 and im.shape[2] == 4:
		im = im[:,:,0].astype(int) \
			+ im[:,:,1].astype(int)*256 \
			+ im[:,:,2].astype(int)*256*256 \
			+ im[:,:,3].astype(int)*256*256*256
	return im



def query_yes_no(question, default="yes"):

    valid = {"yes":True,   "y":True,  "ye":True,
        "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
        	return valid[default]
        elif choice in valid:
        	return valid[choice]
        else:
        	sys.stdout.write("Please respond with 'yes' or 'no' "\
	                         "(or 'y' or 'n').\n")



def UnlockFolder(u_info, dir):
    tmp_open_files4lock = u_info.open_files4lock.get(dir)
    if tmp_open_files4lock is None :
        print('UnlockFolder: folder already open.')
        return False

#    print('Unlock folder: ', dir)
#    for lockfile in tmp_open_files4lock.keys():
#        print('lockfile: ', lockfile)

    for lockfileobj in tmp_open_files4lock.values():
        lockfileobj.close()
    del u_info.open_files4lock[dir]


def LockFolder(u_info, dir):
    if dir in u_info.open_files4lock :
        UnlockFolder(u_info, dir)
    ##
    target1 = glob.glob(path.join(dir,'*'))
    target2 = glob.glob(path.join(dir,'*','*'))
    target_files = filter(lambda f: os.path.isfile(f), target1 + target2)
    tmp_file4lock = {}
    for ofile in target_files:
        # print(ofile)
        try:
            tmp_file4lock[ofile] = open(ofile, 'r+')
        except:
            print("Cannot lock file, but continue..")
            for closefile in tmp_file4lock.values():
                closefile.close()
            return True
    u_info.open_files4lock[dir] = tmp_file4lock


def _LockFolder(u_info, dir):
    if dir in u_info.open_files4lock :
        UnlockFolder(u_info, dir)
    tmp_file4lock = {}
    for curDir, dirs, files in os.walk(dir):
        if files:
            for file in files:
                ofile = f'{curDir}{os.path.sep}{file}'
                try:
                    tmp_file4lock[ofile] = open(ofile, 'r+')
                except:
                    print("Cannot lock file, but continue..")
                    for closefile in tmp_file4lock.values():
                        closefile.close()
                    return True
    u_info.open_files4lock[dir] = tmp_file4lock


def CloseFolder(u_info,  dir):
    tmp_open_files4lock = u_info.open_files4lock[dir]
    for lockfileobj in tmp_open_files4lock.values():
        lockfileobj.close()
    del u_info.open_files4lock[dir]
    u_info.open_files.remove(dir)


# Due to unicode comaptibitiy
# https://qiita.com/SKYS/items/cbde3775e2143cad7455
# 16bit png seems not to be read in "np.fromfile".
# http://jamesgregson.ca/16-bit-image-io-with-python.html

def imread(filename, flags=cv2.IMREAD_UNCHANGED, dtype=None):

    try:

#        n = np.fromfile(filename, dtype)
#        img = cv2.imdecode(n, flags)
#        root, ext = os.path.splitext(filename)
#
#        if ext in ['.png','.PNG']:
#            img = png.Reader(filename).read()
#        elif ext in ['.TIF','.tif', '.TIFF', '.tiff','.png','.PNG','.jpg', '.jpeg','.JPG', '.JPEG']:
#            img = tifffile.imread(filename)
#        else:
#cv2.COLOR_GRAY2RGB

        pil_img = PIL.Image.open(filename)
        img = np.array(pil_img)

        if img.dtype == 'int32':
            img = img.astype('uint16')
        if dtype != None:
            img = img.astype(dtype)
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if flags == cv2.IMREAD_GRAYSCALE:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        elif img.ndim == 1:
            if flags == cv2.IMREAD_COLOR:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

#        print('Image dtype: ', img.dtype,  img.shape)

        return img
    except Exception as e:
        print(e)
        return None




def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False



def ObtainFullSizeImagesPanel(u_info, db, iz):

    target_path = u_info.tile_images_path
    merged_ids = np.zeros((db.canvas_size_y, db.canvas_size_x), u_info.images_dtype)  # type: Any
    iw = 0
    for iy, ix in product(range(db.num_tiles_y), range(db.num_tiles_x)):
        ## Load panels
        tile_filename = target_path + u_info.tile_images_filename_wzyx.format(iw, iz, iy, ix)
        #tile_images = cv2.imread(tile_filename, cv2.IMREAD_UNCHANGED)
        tile_images = PIL.Image.open(tile_filename)

        ## Obtain merged ids
        y = iy * db.num_voxels_per_tile_y
        x = ix * db.num_voxels_per_tile_x
        merged_ids[y: y + db.num_voxels_per_tile_y, x: x + db.num_voxels_per_tile_x] = tile_images
    return merged_ids


def ObtainFullSizeIdsPanel(u_info, db, iz):

    ## try the temporary data first
#    data_path = u_info.tmp_tile_ids_path + u_info.tile_path_wz.format(0, iz)
#    if not os.path.isdir(data_path):
#        target_path = u_info.tile_ids_path
#    else:
#        target_path = u_info.tmp_tile_ids_path

    target_path = u_info.tile_ids_path

    merged_ids = np.zeros((db.canvas_size_y, db.canvas_size_x), u_info.ids_dtype)
    iw = 0
    for iy, ix in product(range(db.num_tiles_y), range(db.num_tiles_x)):
        ## Load panels
        tile_ids_filename = target_path \
                            + u_info.tile_ids_filename_wzyx.format(iw, iz, iy, ix)
        tile_ids = load_hdf5(tile_ids_filename, u_info.tile_var_name)

        ## Obtain merged ids
        y = iy * db.num_voxels_per_tile_y
        x = ix * db.num_voxels_per_tile_x
        merged_ids[y: y + db.num_voxels_per_tile_y, x: x + db.num_voxels_per_tile_x] = tile_ids
    return merged_ids


def SaveFullSizeIdsPanel(u_info, db, iz, merged_ids):

#    u_info.ids_files_undo = []
#    self.flag_undo = 1
#    self.flag_redo = 0
    #target_path = u_info.tmp_ids_path
    #m.mkdir_safe(target_path)
    #target_path = u_info.tmp_tile_ids_path
    #m.mkdir_safe(target_path)

    target_path = u_info.tile_ids_path

    for iw in range(db.num_tiles_w):

        targ = merged_ids[::(2 ** iw), ::(2 ** iw)]

        ## Absorption of zoomlevel dependence of fringe size.
        current_num_voxels_y = db.num_tiles_y_at_w[iw] * db.num_voxels_per_tile_y
        current_num_voxels_x = db.num_tiles_x_at_w[iw] * db.num_voxels_per_tile_x
        current_labels = np.zeros((current_num_voxels_y, current_num_voxels_x), targ.dtype)
        current_labels[0:targ.shape[0], 0:targ.shape[1]] = targ


        for iy, ix in product(range(db.num_tiles_y_at_w[iw]),
                                    range(db.num_tiles_x_at_w[iw])):

            ## Obtain a target id panel
            yid_start = iy * db.num_voxels_per_tile_y
            xid_start = ix * db.num_voxels_per_tile_x
            yid_goal = iy * db.num_voxels_per_tile_y + db.num_voxels_per_tile_y
            xid_goal = ix * db.num_voxels_per_tile_x + db.num_voxels_per_tile_x
            tile_ids = current_labels[yid_start: yid_goal, xid_start: xid_goal]

            ## Set filename
            #target_path2 = target_path + u_info.tile_path_wz.format(iw, iz)
            #m.mkdir_safe(target_path2)
            current_tile_ids_name = target_path \
                            + u_info.tile_ids_filename_wzyx.format(iw, iz, iy, ix)

            # Backup undo
            # shutil.move(current_tile_ids_name, current_tile_ids_name + '_')
            # u_info.ids_files_undo.append(current_tile_ids_name)  ## Filename for undo

            # Make changes
            save_hdf5(current_tile_ids_name, u_info.tile_var_name, tile_ids)


def gen_col_pil(id_data, colordata):
    ncol = id_data.shape[0]
    nrow = id_data.shape[1]
    imgArray = np.zeros((ncol, nrow, 3), dtype='uint8')
    for i in range(ncol):
        for j in range(nrow):
            imgArray[i, j][0] = colordata[id_data[i, j], 0]  # R
            imgArray[i, j][1] = colordata[id_data[i, j], 1]  # G
            imgArray[i, j][2] = colordata[id_data[i, j], 2]  # B
    pilOUT = PIL.Image.fromarray(np.uint8(imgArray))
    return pilOUT

def save_tifc(id_data, filename, colordata):
    pilOUT = gen_col_pil(id_data, colordata)
    pilOUT.save(filename)

def save_pngc(id_data, filename, colordata):
    pilOUT = gen_col_pil(id_data, colordata)
    pilOUT.save(filename)

def save_npy(self, id_data, filename):
    np.save(filename, id_data)

'''
def save_tif_rgb(id_data, filename):
	if id_data.()

    imwrite(filename, id_data.astype('uint16'))
'''

def save_tif16(id_data, filename):
    imwrite(filename, id_data.astype('uint16'))

def save_tif24(id_data, filename):
    pilOUT = PIL.Image.fromarray(np.uint8(id_data))
    pilOUT.save(filename)

def save_tif8(id_data, filename, compression=5):

    # int(cv.IMWRITE_TIFF_COMPRESSION) == 1: No compression
    # int(cv.IMWRITE_TIFF_COMPRESSION) == 5: Lempel-Ziv & Welch (LZW) compression

    if compression == 5:
        imwrite(filename, id_data.astype('uint8') )
    else :
        imwrite(filename, id_data.astype('uint8'), params=( int(cv2.IMWRITE_TIFF_COMPRESSION), compression) )

    # pilOUT = PIL.Image.fromarray(np.uint8(tile_image))
    # pilOUT.save(current_tile_image_name)


def save_jpg16(id_data, filename):
    imwrite(filename, id_data.astype('uint16'))

def save_jpg8(id_data, filename):
    imwrite(filename, id_data.astype('uint8'))

def save_png16(id_data, filename):
    # Use pypng to write zgray as a grayscale PNG.
    with open(filename, 'wb') as f:
        writer = png.Writer(width=id_data.shape[1], height=id_data.shape[0], bitdepth=16, greyscale=True)
        id_data_list = id_data.astype('uint16').tolist()
        writer.write(f, id_data_list)

def save_png8(id_data, filename):
    # Use pypng to write zgray as a grayscale PNG.
    with open(filename, 'wb') as f:
        writer = png.Writer(width=id_data.shape[1], height=id_data.shape[0], bitdepth=8, greyscale=True)
        id_data_list = id_data.astype('uint8').tolist()
        writer.write(f, id_data_list)

def mkdir_safe( dir_to_make ):
    if not os.path.exists( dir_to_make ):
        if os.name == 'nt':
            execute_string = 'mkdir ' + '"' + str(dir_to_make) + '"'
        else :
            execute_string = 'mkdir -p ' + '"' + str(dir_to_make) + '"'
        os.system( execute_string )


def load_hdf5(file_path, dataset_name):
    hdf5 = h5py.File(file_path, 'r')
    array = hdf5[dataset_name][()]
    hdf5.close()
    return array

def save_hdf5( file, dataset_name, array ):
    hdf5             = h5py.File( file, 'w' )
    hdf5.create_dataset( dataset_name, data=array )
    hdf5.flush()
    hdf5.close()

def ObtainImageFiles(input_path):
    Image_files = []
    files_in_folder = glob.glob(os.path.join(input_path, "*"))
    for file in files_in_folder:
        root, ext = os.path.splitext(file)
        if ext in ['.TIF','.tif', '.TIFF', '.tiff','.png','.PNG','.jpg', '.jpeg','.JPG', '.JPEG'] :
            Image_files.append(file)

    Image_files = sorted(Image_files)
    return Image_files


def SaveImage(output_image, filename):
    output_dtype = output_image.dtype
    root, ext = os.path.splitext(filename)
    if ext in ['.TIF','.tif', '.TIFF', '.tiff']:
        if output_dtype == 'uint16':
            save_tif16(output_image, filename)
        elif output_dtype == 'uint8':
            save_tif8(output_image, filename)
        else:
            print('dtype mismatch: ', ext, output_dtype)
            return False
    elif ext in ['.png','.PNG']:
        if output_dtype == 'uint16':
            save_png16(output_image, filename)
        elif output_dtype == 'uint8':
            save_png8(output_image, filename)
        else:
            print('dtype mismatch: ', ext, output_dtype)
            return False
    elif ext in ['.jpg', '.jpeg','.JPG', '.JPEG']:
        if output_dtype == 'uint16':
            save_jpg16(output_image, filename)
        elif output_dtype == 'uint8':
            save_jpg8(output_image, filename)
        else:
            print('dtype mismatch: ', ext, output_dtype)
            return False

    return True


