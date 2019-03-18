import os
import sys
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
_dojo_dir = path.join(main_dir, "gui")
sys.path.append(_dojo_dir)

from Credit  import Credit
from ExportIdDialog import ExportIdDialog
from ExportImageDialog import ExportImageDialog
from FileIO  import FileIO
from FileMenu  import FileMenu
from func_persephonep import *
from ImportDialog import ImportDialog
from MainWindow import MainWindow
from Script  import Script

