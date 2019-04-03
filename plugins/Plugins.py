import sys
import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0])) # Dir of main
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)

# ------------------------------------------------------------
# Plugin Interface
# Please add user defined functions
# Also edit "menu.json" for a plugins pulldown menu.
# ------------------------------------------------------------

sys.path.append(path.join(plugins_dir, "_3D_filters"))
sys.path.append(path.join(plugins_dir, "_2D_filters"))
sys.path.append(path.join(plugins_dir, "Template"))
from Dialog_3D_Filters import Dialog_3D_Filters
from Dialog_2D_Filters import Dialog_2D_Filters
from Dialog_Template   import Dialog_Template

# import wxglade_superpixel

class Plugins():

    def _2D_Filters(self):
        self.tmp = Dialog_2D_Filters(self)

    def _3D_Filters(self):
        self.tmp = Dialog_3D_Filters(self)

    def Template(self):
        self.tmp = Dialog_Template(self)

    def UserDefined_(self):
        print("'User Defined' is not implemented!")


# ----------------------------------------------------------------------

