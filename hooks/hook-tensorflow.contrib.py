import os
from PyInstaller.utils.hooks import get_package_paths
from PyInstaller.compat import is_linux


def collect_native_files(package, files):
    pkg_base, pkg_dir = get_package_paths(package)
    return [(os.path.join(pkg_dir, file), package.replace('.', os.path.sep)) for file in files]


if is_linux:
    datas = collect_native_files('tensorflow.contrib.bigtable.python.ops', ['_bigtable.so'])