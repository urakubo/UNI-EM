import optparse

parser = optparse.OptionParser(
    usage="usage: %runServer [annotator | dojo] [dojo folder]")
(options, args) = parser.parse_args()
(server_type, relative_dojo_dir) = args

if len(args) != 2:
  parser.error("Invalid arguments")
elif server_type != 'annotator' and server_type != 'dojo':
  parser.error("Server type should be annotator or dojo")

from os import path
import sys
import numpy as np

main_dir = path.abspath(path.join(path.dirname(sys.argv[0])))
sys.path.append(main_dir)
sys.path.append(path.join(main_dir, "system"))
sys.path.append(path.join(main_dir, "dojo"))
sys.path.append(path.join(main_dir, "dojoio"))
sys.path.append(path.join(main_dir, "annotator"))
sys.path.append(path.join(main_dir, "segment"))
sys.path.append(path.join(main_dir, "plugins"))

from Params import Params
from Annotator.AnnotatorServer import AnnotatorServerLogic
from DojoServer import ServerLogic

dojo_dir = path.abspath(path.join(main_dir, relative_dojo_dir))
params = Params()
params.SetUserInfo(dojo_dir)
params.SetUserInfoAnnotator(dojo_dir)

if server_type == 'annotator':
  logic = AnnotatorServerLogic(params)
  logic.run()
elif server_type == 'dojo':
  logic = ServerLogic()
  logic.run(params)
else:
  parse.error("Server type should be annotator or dojo")