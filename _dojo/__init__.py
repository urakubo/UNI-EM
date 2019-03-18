import os
import sys
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
_dojo_dir = path.join(main_dir, "_dojo")
sys.path.append(_dojo_dir)
# parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
# icon_dir    = path.join(parent_dir, "icons")
# sys.path.append(path.join(parent_dir, "Plugins"))

from image import Image
from segmentation import Segmentation
from viewer import Viewer
from setup import Setup
from websockets import Websockets
from controller import Controller
from database import Database
