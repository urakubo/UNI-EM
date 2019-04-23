# -*- mode: python -*-
import sys
from os import path, pardir
main_dir = os.path.abspath(SPECPATH)
main_dir = os.path.dirname(main_dir)
block_cipher = None


import tensorboard as _
WEBFILES = os.path.join(_.__path__[0], "webfiles.zip")

tensorb=[path.join(main_dir, "segment","tensorboard","tensorb.py")]
pathex=[]

print(tensorb)

a = Analysis(tensorb,
             pathex=pathex,
             binaries=[],
             datas=[ ( WEBFILES, './tensorboard/' ) ],
             hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','tensorflow.contrib'],
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
          name='tensorb',
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
               name='tensorb')
