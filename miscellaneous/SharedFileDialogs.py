#
import sys, os, time
import glob
import numpy as np
from os import path, pardir

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "filesystem"))
import miscellaneous.Miscellaneous as m
from PyQt5.QtWidgets import QFileDialog



class SharedFileDialogs():

    def browse_dir_img(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        Dialog = m.Dialog_ImageFolder(self.parent, "Select Image Folder", currentdir)
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
        Dialog = m.Dialog_ImageFolder(self.parent, "Select Image Folder", currentdir)
        return_flag = Dialog.w.exec_()
        if return_flag != 1:
            return False
        open_folder_name = Dialog.GetValue()

        ## Check & open folder
        if len(open_folder_name) == 0:
            return
        open_folder_name = open_folder_name.replace('/', os.sep)
        check_sucess = self.parent.parent.OpenImageFolder(open_folder_name)
        if check_sucess == False:
            return False

        lineedit_obj.addItem(open_folder_name)
        id = lineedit_obj.findText(open_folder_name)
        lineedit_obj.setCurrentIndex(id)

        return True


    def browse_OpenDojoFolder(self, lineedit_obj):
        currentdir = lineedit_obj.currentText()
        if len(currentdir) == 0:
            currentdir = os.path.normpath(main_dir)
        ## Custum image folder
        open_folder_name = QFileDialog.getExistingDirectory(self.parent, "Select Folder", currentdir)

        ## Check & open folder
        if len(open_folder_name) == 0:
            return
        open_folder_name = open_folder_name.replace('/', os.sep)
        check_sucess = self.parent.parent.OpenDojoFolder(open_folder_name)
        if check_sucess == False:
            return False

        #lineedit_obj.addItem(open_folder_name)
        id = lineedit_obj.findText(open_folder_name)
        lineedit_obj.setCurrentIndex(id)
        return True


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
            elif args[i][1] == 'SelectOpenImage':
                param = obj_args[i].currentText()
            params[args_header[i]] = param
        return params




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
            elif args[i][1] == 'SelectOpenImage':
                param = obj_args[i].currentText()
                print("{0:>20} : {1:s}".format(arg, param))
