# -*- mode: python -*-
import sys
from os import path, pardir
main_dir = os.path.abspath(SPECPATH)
main_dir = os.path.dirname(main_dir)
block_cipher = None

pathex=[]
for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment","_3D_FFN","ffn") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

translate=[path.join(main_dir, "segment","_3D_FFN","ffn","train.py")]
print(translate)

a = Analysis(translate,
             pathex=pathex,
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','PyQt5.sip','gast','astor','termcolor','google.protobuf.wrappers_pb2','tensorflow.contrib'],
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
          name='train',
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
               name='train')
