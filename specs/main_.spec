# -*- mode: python -*-
import os, sys
from os import path, pardir
main_dir = os.path.abspath(SPECPATH)
main_dir = os.path.dirname(main_dir)
block_cipher = None

pathex=[
				main_dir,
				path.join(main_dir, "filesystem"),
				path.join(main_dir, "_dojo"),
				path.join(main_dir, "annotator"),
				path.join(main_dir, "gui"),
				path.join(main_dir, "plugins"),
				path.join(main_dir, "segment")]
for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "plugins") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "plugins", dirpath))

for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))


a = Analysis(['./../main.py'],
             pathex=pathex,
             binaries=[],
             datas=[
                      ( '../annotator/menu.json', './annotator/' ),
                      ( '../plugins/menu.json', './plugins/' ),
                      ( '../icons/*', './icons/' ),
                      ( '../icons/Disabled/*', './icons/Disabled/' ),
                      ( '../segment/menu.json', './segment/' )
                    ],
             hiddenimports=['scipy._lib.messagestream',
                      'pywt._extensions._cwt',
                      'PyQt5.sip',
                      'numpy.core._dtype_ctypes',
                      'gast',
                      'tensorflow.contrib.batching',
                      'tensorflow.python.autograph'
                      ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
