
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib.util
from importlib import machinery
import sys
import os
from os import path, pardir
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QInputDialog, QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))
import importlib.util


class Script():
    def Script(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', main_dir, filter='*.py')
        if len(filename[0]) == 0:
            return
        print('Execute file: ')
        print(filename[0])

        # spec = importlib.util.spec_from_file_location(os.path.basename(filename[0]), os.path.dirname(filename[0]))
        # foo = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(foo)

        #foo = importlib.import_module(filename[0])
        #foo.MyClass(self)

#        loader = machinery.SourceFileLoader('MyClass', filename[0])
#        module = loader.load_module()
#        module.MyClass(self)
#        module = None
#        print(module)

        try:
            exec(open(filename[0]).read())
        except SyntaxError as err:
            print('Syntax error. Line ', err.lineno)
