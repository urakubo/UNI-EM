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

sys.path.append(path.join(plugins_dir, "Filters"))
sys.path.append(path.join(plugins_dir, "Template"))
from Dialog_Filters  import Dialog_Filters
from Dialog_Template import Dialog_Template


class Plugins():

    def Filters(self):
        self.tmp = Dialog_Filters(self)

    def Template(self):
        self.tmp = Dialog_Template(self)

    def UserDefined_(self):
        print("'User Defined' is not implemented!")


# ----------------------------------------------------------------------

