# Only for tensorboard 1.15
# Modified from :
# C:\Users\uraku\AppData\Local\Programs\Python\Python38\Lib\site-packages\tensorboard\main.py

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main


# pylint: disable=g-import-not-at-top
import os

# Disable the TF GCS filesystem cache which interacts pathologically with the
# pattern of reads used by TensorBoard for logdirs. See for details:
#   https://github.com/tensorflow/tensorboard/issues/1225
# This must be set before the first import of tensorflow.
os.environ['GCS_READ_CACHE_DISABLED'] = '1'
# pylint: enable=g-import-not-at-top

import sys

from tensorboard import default
from tensorboard import program
from tensorboard.compat import tf
from tensorboard.plugins import base_plugin
from tensorboard.util import tb_logging


logger = tb_logging.get_logger()

def run_main():
  """Initializes flags and calls main()."""
  program.setup_environment()

  if getattr(tf, '__version__', 'stub') == 'stub':
    print("TensorFlow installation not found - running with reduced feature set.",
          file=sys.stderr)

  ##
  webfiles = path.join(main_dir,'tensorboard','webfiles.zip')
  ##

  tensorboard = program.TensorBoard(
      default.get_plugins() + default.get_dynamic_plugins(),
      lambda: open(webfiles, 'rb'))
  try:
    from absl import app
    # Import this to check that app.run() will accept the flags_parser argument.
    from absl.flags import argparse_flags
    app.run(tensorboard.main, flags_parser=tensorboard.configure)
    raise AssertionError("absl.app.run() shouldn't return")
  except ImportError:
    pass
  except base_plugin.FlagsError as e:
    print("Error: %s" % e, file=sys.stderr)
    sys.exit(1)

  tensorboard.configure(sys.argv)
  sys.exit(tensorboard.main())


if __name__ == '__main__':
  run_main()


