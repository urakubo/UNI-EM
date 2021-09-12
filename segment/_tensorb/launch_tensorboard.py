# Only for tensorboard 1.15
# Modified from :
# C:\Users\uraku\AppData\Local\Programs\Python\Python38\Lib\site-packages\tensorboard\main.py

import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
webfiles = path.join(main_dir,'tensorboard','webfiles.zip')


# pylint: disable=g-import-not-at-top


# Disable the TF GCS filesystem cache which interacts pathologically with the
# pattern of reads used by TensorBoard for logdirs. See for details:
#   https://github.com/tensorflow/tensorboard/issues/1225
# This must be set before the first import of tensorflow.
os.environ['GCS_READ_CACHE_DISABLED'] = '1'
# pylint: enable=g-import-not-at-top

from absl import app
from tensorboard import default
from tensorboard import main_lib
from tensorboard import program
from tensorboard.plugins import base_plugin
from tensorboard.uploader import uploader_subcommand
from tensorboard.util import tb_logging

logger = tb_logging.get_logger()



def run_main():
    """Initializes flags and calls main()."""
    main_lib.global_init()

    tensorboard = program.TensorBoard(
        plugins=default.get_plugins(),
        assets_zip_provider=lambda: open(webfiles, 'rb'),
        subcommands=[uploader_subcommand.UploaderSubcommand()],
    )
    try:
        app.run(tensorboard.main, flags_parser=tensorboard.configure)
    except base_plugin.FlagsError as e:
        print("Error: %s" % e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run_main()



