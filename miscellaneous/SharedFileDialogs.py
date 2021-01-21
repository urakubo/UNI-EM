#
import sys, os, time
import glob
import numpy as np
import pickle
import fnmatch
from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "system"))
import miscellaneous.DialogImageFolder as d
from PyQt5.QtWidgets import QFileDialog


class SharedFileDialogs():

    def browse_dir_img(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        Dialog = d.DialogImageFolder(self.parent, "Select Image Folder", currentdir)
        return_flag = Dialog.w.exec_()
        if return_flag == 1:
            newdir = Dialog.GetValue()
            lineedit_obj.setText(newdir)
            return True
        return False

    def browse_dir(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        newdir = QFileDialog.getExistingDirectory(self.parent, "Select Folder", currentdir)
        if len(newdir) == 0:
            return False
        newdir = newdir.replace('/', os.sep)
        lineedit_obj.setText(newdir)
        return True

    def browse_file(self, lineedit_obj):
        currentfile = lineedit_obj.text()
        newfile = QFileDialog.getOpenFileName(self.parent, "Select File", currentfile)
        newfile = newfile[0]
        if len(newfile) == 0:
            return False
        newfile = newfile.replace('/', os.sep)
        lineedit_obj.setText(newfile)
        return True

    def browse_OpenImageFolder(self, lineedit_obj):
        currentdir = lineedit_obj.currentText()
        if len(currentdir) == 0:
            currentdir = os.path.normpath(main_dir)
        ## Custum image folder
        Dialog = d.DialogImageFolder(self.parent, "Select Image Folder", currentdir)
        return_flag = Dialog.w.exec_()
        if return_flag != 1:
            return False
        open_folder_name = Dialog.GetValue()

        ## Check & open folder
        if len(open_folder_name) == 0:
            return
        open_folder_name = open_folder_name.replace('/', os.sep)
        check_sucess = self.parent.parent.OpenSpecificFolder(open_folder_name, ['png','tif','jpg'])
        if check_sucess == False:
            id = lineedit_obj.findText(open_folder_name)
            if id >= 0:
            	lineedit_obj.setCurrentIndex(id)
            	return True
            return False

#        lineedit_obj.addItem(open_folder_name)
        id = lineedit_obj.findText(open_folder_name)
        lineedit_obj.setCurrentIndex(id)

        return True




    def browse_OpenSpecificFile(self, lineedit_obj, file_type):
        currentdir = lineedit_obj.currentText()
        if len(currentdir) == 0:
            currentdir = os.path.normpath(main_dir)
        else :
            currentdir = os.path.dirname(currentdir)
        ## Folder dialog.
        open_file_name = QFileDialog.getOpenFileName(self.parent, "Select File", currentdir)

#        print('open_file_name: ', open_file_name)

        ## Check & open folder
        if len(open_file_name) == 0:
            return
        open_file_name = open_file_name[0].replace('/', os.sep)

        check_sucess = self.parent.parent.OpenSpecificFolder(open_file_name, file_type)

        if check_sucess == False:
            id = lineedit_obj.findText(open_file_name)
            if id >= 0:
            	lineedit_obj.setCurrentIndex(id)
            	return True
            return False

#        lineedit_obj.addItem(open_file_name)
        id = lineedit_obj.findText(open_file_name)
        lineedit_obj.setCurrentIndex(id)

        return True


    def browse_OpenSpecificFolder(self, lineedit_obj, folder_type):
        currentdir = lineedit_obj.currentText()
        if len(currentdir) == 0:
            currentdir = os.path.normpath(main_dir)
        else :
            currentdir = os.path.dirname(currentdir)
        ## Folder dialog.
        open_folder_name = QFileDialog.getExistingDirectory(self.parent, "Select Folder", currentdir)

        ## Check & open folder
        if len(open_folder_name) == 0:
            return
        open_folder_name = open_folder_name.replace('/', os.sep)

        check_sucess = self.parent.parent.OpenSpecificFolder(open_folder_name, folder_type)

        if check_sucess == False:
            id = lineedit_obj.findText(open_folder_name)
            if id >= 0:
            	lineedit_obj.setCurrentIndex(id)
            	return True
            return False

#        lineedit_obj.addItem(open_folder_name)
        id = lineedit_obj.findText(open_folder_name)
        lineedit_obj.setCurrentIndex(id)

        return True


    ##
    ##
    def ObtainImageFiles(self, input_path):
        #
        search1 = os.path.join(input_path, '*.png')
        search2 = os.path.join(input_path, '*.tif')
        search3 = os.path.join(input_path, '*.tiff')
        filestack = sorted(glob.glob(search1))
        filestack.extend(sorted(glob.glob(search2)))
        filestack.extend(sorted(glob.glob(search3)))
        return filestack
    ##
    ##
    def ObtainParams(self, obj_args, args):
    
        args_header = [args[i][0] for i in range(len(args))]
        params = {}
        for i, arg in enumerate(args):
            param = {}
            if args[i][1] == 'LineEdit':
                param = obj_args[i].text()
            elif args[i][1] == 'SpinBox':
                param = np.str( obj_args[i].value() )
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
            elif args[i][1] == 'Tab':
                id = obj_args[i].currentIndex()
                param = obj_args[i].tabText(id)
            elif args[i][1] == 'CheckBox':
                param = obj_args[i].checkState()
            elif fnmatch.fnmatch(args[i][1], 'Select*Folder') :
                param = obj_args[i].currentText()
            params[args_header[i]] = param
        # print(params)
        return params
    ##
    ##
    def print_current_states(self, obj_args, args, args_title):
        for i, arg in enumerate(args_title):
            if args[i][1] == 'LineEdit':
                param = obj_args[i].text()
                print("{0:>20} : {1:s}".format(arg, param))
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
                print("{0:>20} : {1:d}".format(arg, param))
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
                print("{0:>20} : {1:s}".format(arg, param))
            elif args[i][1] == 'CheckBox':
                param = obj_args[i].checkState()
                print("{0:>20} : {1:d}".format(arg, param))
            elif fnmatch.fnmatch(args[i][1], 'Select*Folder') :
                param = obj_args[i].currentText()
                print("{0:>20} : {1:s}".format(arg, param))


    def save_params(self, obj_args, args, title):
        #
        args_header = [args[i][0] for i in range(len(args))]
        id = args_header.index('Save Parameters')
        filename = obj_args[id].text()
        params = self.ObtainParams(obj_args, args)

        print('')
        print('Save file : ', filename)
        self.print_current_states(obj_args, args, args_header)
        print('')
        try:
            with open(filename, mode='wb') as f:
                pickle.dump(params, f)
            print(title, ': Parameter file was saved.')
        except:
            print(title, ': Parameter file could not be saved.')
            return False

        return True


    def load_params(self, obj_args, args, title):
        #
        args_header = [args[i][0] for i in range(len(args))]
        id = args_header.index('Load Parameters')
        filename = obj_args[id].text()
        print('')
        print('Load file : ', filename)
        try:
            with open(filename, mode='rb') as f:
                params = pickle.load(f)
        except:  # parent of IOError, OSError *and* WindowsError where available
            print(title, ': Parameter file cannot be open.')
            return False

        for i, arg in enumerate(args_header):
            if args[i][1] == 'LineEdit':
                obj_args[i].setText(params[args_header[i]])
            elif args[i][1] == 'SpinBox':
                #print(params[args_header[i]])
                obj_args[i].setValue(int(params[args_header[i]]))
            elif args[i][1] == 'ComboBox':
                id = obj_args[i].findText(params[args_header[i]])
                obj_args[i].setCurrentIndex(id)
            elif args[i][1] == 'Tab':
                obj_args[i].setCurrentIndex(  args[i][2].index(params[args_header[i]])  )
            elif args[i][1] == 'CheckBox':
                obj_args[i].setCheckState(params[args_header[i]])

        self.print_current_states(obj_args, args, args_header)
        return True


