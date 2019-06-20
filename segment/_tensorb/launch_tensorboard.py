from tensorboard import default
from tensorboard import program
from argparse import ArgumentParser
# import socket
import time


usage = 'Usage: python tensorb [--logdir] [--host]'
argparser = ArgumentParser(usage=usage)
argparser.add_argument('--logdir', type=str,
                           help='')
argparser.add_argument('--host', type=str,
                           help='')
args = argparser.parse_args()

argv=[None, '--logdir', args.logdir,'--host', args.host]
#print(argv)
tb = program.TensorBoard(default.get_plugins(), default.get_assets_zip_provider())
tb.configure(argv=argv)
tb.launch()
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print('Tensorboard interrupted!')

