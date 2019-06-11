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
from itertools import product
import glob

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

def UnlockFolder(u_info, dir):
    tmp_open_files4lock = u_info.open_files4lock[dir]
    for lockfileobj in tmp_open_files4lock.values():
        lockfileobj.close()
    del u_info.open_files4lock[dir]


def LockFolder(u_info, dir):
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
                    print("Cannot lock file.")
                    for closefile in tmp_file4lock.values():
                        closefile.close()
                    return False
    u_info.open_files4lock[dir] = tmp_file4lock



def CloseFolder(u_info,  dir):
    tmp_open_files4lock = u_info.open_files4lock[dir]
    for lockfileobj in tmp_open_files4lock.values():
        lockfileobj.close()
    del u_info.open_files4lock[dir]
    u_info.open_files.remove(dir)



# https://qiita.com/SKYS/items/cbde3775e2143cad7455

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
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
        tile_ids = m.load_hdf5(tile_ids_filename, u_info.tile_var_name)

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
            m.save_hdf5(current_tile_ids_name, u_info.tile_var_name, tile_ids)


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

def save_tif16(id_data, filename):
    cv2.imwrite(filename, id_data.astype('uint16'))

def save_tif8(id_data, filename):
    cv2.imwrite(filename, id_data.astype('uint8'))
    # pilOUT = PIL.Image.fromarray(np.uint8(tile_image))
    # pilOUT.save(current_tile_image_name)

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
        execute_string = 'mkdir ' + '"' + dir_to_make + '"'
        #print(execute_string)
        os.system( execute_string )


def load_hdf5(file_path, dataset_name):
    hdf5 = h5py.File(file_path, 'r')
    array = hdf5[dataset_name].value
    hdf5.close()
    return array

def save_hdf5( file, dataset_name, array ):
    hdf5             = h5py.File( file, 'w' )
    hdf5.create_dataset( dataset_name, data=array )
    hdf5.flush()
    hdf5.close()

def ObtainImageFiles(input_path):
    search1 = os.path.join(input_path, '*.png')
    search2 = os.path.join(input_path, '*.tif')
    search3 = os.path.join(input_path, '*.tiff')
    filestack = sorted(glob.glob(search1))
    filestack.extend(sorted(glob.glob(search2)))
    filestack.extend(sorted(glob.glob(search3)))
    return filestack


class _MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DecorationRole:
            return QIcon(QPixmap(self.listdata[index.row()]))
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(os.path.splitext(os.path.split(self.listdata[index.row()])[-1])[0])
        else:
            return QVariant()

class Dialog_ImageFolder():
    def __init__(self, parent, title, init_path):
        self.w = QDialog(parent)

        self.parent = parent
        self.left   = 300
        self.top    = 300
        self.width  = 600
        self.height = 400
        self.title  = title

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(init_path)
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.treeview = QTreeView()
        self.treeview.setModel(self.dirModel)
        self.treeview.setRootIndex(self.dirModel.index(""))
        self.treeview.clicked.connect(self.on_clicked)
        #--- Hide All Header Sections Except First ----
        header = self.treeview.header()
        for sec in range(1, header.count()):
            header.setSectionHidden(sec, True)
        #--- ---- ---- ---- ---- ---- ---- ---- ---- --

        focus_index = self.dirModel.index(init_path)
        self.treeview.setCurrentIndex(focus_index)
        self.current_row_changed()

        self.listview = QListView()
        self.listview.setViewMode(QListView.IconMode)
        self.listview.setIconSize(QSize(192,192))

        targetfiles1 =  glob.glob(os.path.join( init_path, '*.png'))
        targetfiles2 =  glob.glob(os.path.join( init_path, '*.tif'))
        targetfiles3 =  glob.glob(os.path.join( init_path, '*.tiff'))
        targetfiles  = targetfiles1 + targetfiles2 + targetfiles3
        lm = _MyListModel(targetfiles, self.parent)
        self.listview.setModel(lm)

        self.sub_layout = QHBoxLayout()
        self.sub_layout.addWidget(self.treeview)
        self.sub_layout.addWidget(self.listview)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.sub_layout)
        self.main_layout.addWidget(self.buttonBox)

        self.w.setGeometry(self.left, self.top, self.width, self.height)
        self.w.setWindowTitle(self.title)
        self.w.setWindowIcon(QIcon(os.path.join(icon_dir, 'Mojo2_16.png')))
        self.w.setLayout(self.main_layout)

    def current_row_changed(self):
        index = self.treeview.currentIndex()
        self.treeview.scrollTo(index, QAbstractItemView.EnsureVisible)
        self.treeview.resizeColumnToContents(0)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()

        targetfiles1 =  glob.glob(os.path.join( path, '*.png'))
        targetfiles2 =  glob.glob(os.path.join( path, '*.tif'))
        targetfiles3 =  glob.glob(os.path.join( path, '*.tiff'))
        targetfiles  = targetfiles1 + targetfiles2 + targetfiles3

        lm = _MyListModel(targetfiles, self.parent)
        self.listview.setModel(lm)

    def accept(self):
        index = self.treeview.currentIndex()
        self.newdir = self.dirModel.filePath(index)
        self.w.done(1)

    def reject(self):
        self.w.done(0)

    def GetValue(self):
        index = self.treeview.currentIndex()
        self.newdir = self.dirModel.filePath(index)
        return self.newdir
