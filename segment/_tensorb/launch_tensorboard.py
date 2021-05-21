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
# import socket
import time

logger = tb_logging.get_logger()
program.setup_environment()

from argparse import ArgumentParser
usage = 'Usage: python tensorb [--logdir] [--host]'
argparser = ArgumentParser(usage=usage)
argparser.add_argument('--logdir', type=str,
                           help='')
argparser.add_argument('--host', type=str,
                           help='')
args = argparser.parse_args()

argv=[None, '--logdir', args.logdir,'--host', args.host]

tb = program.TensorBoard(default.get_plugins() + default.get_dynamic_plugins(), program.get_default_assets_zip_provider())
tb.configure(argv=argv)
tb.launch()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Tensorboard interrupted!')

