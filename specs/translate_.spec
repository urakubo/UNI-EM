# -*- mode: python -*-
import sys
from os import path, pardir
main_dir = os.path.abspath(SPECPATH)
main_dir = os.path.dirname(main_dir)
block_cipher = None

pathex=[path.join(main_dir, "segment","_2D_DNN")]
translate=[path.join(main_dir, "segment","_2D_DNN","translate.py")]
print(translate)

a = Analysis(translate,
             pathex=pathex,
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','PyQt5.sip','tensorflow.contrib'],
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
          name='translate',
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
               name='translate')
