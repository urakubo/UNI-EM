###
###
###
import sys, os, time, errno
import subprocess as s
import glob
import cv2


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
import miscellaneous.Miscellaneous as m
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))


class InferenceTab():

    def _Run(self, parent, params, comm_title):

        datadir = parent.u_info.data_path

        input_files = glob.glob(os.path.join(params['Image Folder'], "*.jpg"))
        input_png = glob.glob(os.path.join(params['Image Folder'], "*.png"))
        input_tif = glob.glob(os.path.join(params['Image Folder'], "*.tif"))
        input_files.extend(input_png)
        input_files.extend(input_tif)
        if len(input_files) == 0:
            print('No images in the Image Folder.')
            return

        im = cv2.imread(input_files[0], cv2.IMREAD_UNCHANGED)
        print('Target file to check color type : ', input_files[0])
        print('Image dimensions                : ', im.shape)
        print('Image filetype                  : ', im.dtype)
        image_width  = im.shape[1]
        image_height = im.shape[0]

        if not (im.dtype == "uint8" and len(im.shape) == 3 and  input_tif == []) :
            tmpdir = os.path.join(datadir, "tmp", "DNN_test_images")
            if os.path.exists(tmpdir) :
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            for input_file in input_files:
                im_col = cv2.imread(input_file)
                filename = os.path.basename(input_file)
                filename = filename.replace('.tif', '.png')
                converted_input_file = os.path.join( tmpdir, filename )
                cv2.imwrite(converted_input_file, im_col)
            params['Image Folder'] = tmpdir
            print('Filetype of images was changed to RGB 8bit, and stored in ', tmpdir)


        comm = parent.u_info.exec_translate +' ' \
                + ' --mode predict ' \
                + ' --save_freq 0 ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
                + ' --output_dir ' + params['Output Segmentation Folder'] + ' ' \
                + ' --checkpoint ' + params['Model Folder'] + ' ' \
                + ' --image_height ' + str(image_height) + ' ' \
                + ' --image_width ' + str(image_width)

        try:
            print(comm)
            print('Start inference.')
            m.UnlockFolder(parent.u_info, params['Output Segmentation Folder'])  # Only for shared folder/file
            s.call(comm.split())
            m.LockFolder(parent.u_info, params['Output Segmentation Folder'])
            return
        except s.CalledProcessError as e:
            print("Inference was not executed.")
            m.LockFolder(parent.u_info, params['Output Segmentation Folder'])
            return


    def __init__(self, u_info):

        modelpath =  u_info.tensorflow_model_path
        self.paramfile =  os.path.join( u_info.parameters_path, "Inference_2D.pickle")

        self.title = '2D Inference'

        self.tips = [
                        'Path to folder containing images',
                        'Path to folder for storing segmentation',
                        'Directory with checkpoint for training data'
                        ]


        self.args = [
                        ['Image Folder',    'SelectImageFolder', 'OpenImageFolder'],
                        ['Output Segmentation Folder',   'SelectImageFolder', 'OpenImageFolder'],
                        ['Model Folder',      'LineEdit', modelpath, 'BrowseDir']
                        ]



