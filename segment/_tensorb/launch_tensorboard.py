#import warnings
#warnings.filterwarnings('ignore', category=DeprecationWarning)
#warnings.filterwarnings('ignore', category=FutureWarning)

# Only for tensorboard 1.14

import sys

from tensorboard import default
from tensorboard import program
from tensorboard.compat import tf
from tensorboard.plugins import base_plugin
from tensorboard.util import tb_logging

from argparse import ArgumentParser
# import socket
import time
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main

usage = 'Usage: python tensorb [--logdir] [--host]'
argparser = ArgumentParser(usage=usage)
argparser.add_argument('--logdir', type=str,
                           help='')
argparser.add_argument('--host', type=str,
                           help='')
args = argparser.parse_args()

argv=[None, '--logdir', args.logdir,'--host', args.host]

logger = tb_logging.get_logger()
program.setup_environment()

# See
# Tensorboard/program.py: get_default_assets_zip_provider

webfiles = path.join(main_dir,'tensorboard','webfiles.zip')
tb = program.TensorBoard(default.get_plugins() + default.get_dynamic_plugins(), lambda: open(webfiles, 'rb'))
tb.configure(argv=argv)
tb.launch()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Tensorboard interrupted!')

