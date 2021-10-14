import os
from PyInstaller.utils.hooks import get_package_paths
from PyInstaller.compat import is_linux


#def collect_native_files(package, files):
#    pkg_base, pkg_dir = get_package_paths(package)
#    return [(os.path.join(pkg_dir, file), package.replace('.', os.path.sep)) for file in files]


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string


if is_linux:
    pkg_base, pkg_dir = get_package_paths('tensorflow.contrib')
    # Walk through all file in the given package, looking for data files.
    _datas = []
    for dirpath, dirnames, files in os.walk(pkg_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            print(extension)
            if extension in ['.so']:
                source = os.path.join(dirpath, f)
                dest = remove_prefix(dirpath,
                                     os.path.dirname(pkg_base) + str(os.sep))
                _datas.append((source, dest))
    #datas = collect_native_files('tensorflow.contrib.bigtable.python.ops', ['_bigtable.so'])
    print(_datas)
    datas = _datas