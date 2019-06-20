# -*- mode: python -*-
import os, sys
from os import path, pardir
main_dir = os.path.abspath(SPECPATH)
main_dir = os.path.dirname(main_dir)

block_cipher = None

def analysis(_spec_path_list, _pathex, _datas, _hiddenimports, _name):
    """
    Do analyized spec file and get analyized data and exe binary data.
    """

    print(f'##### Analyzed {_spec_path_list} #####')

    a = Analysis(_spec_path_list,
                 pathex=_pathex,
                 binaries=[],
                 datas=_datas,
                 hiddenimports=_hiddenimports,
                 hookspath=['./hooks'],
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
              name=_name,
              debug=False,
              strip=False,
              upx=True,
              console=True )

#    coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='main')

    return (exe, a.binaries, a.zipfiles, a.datas) 


coll = ()

########################## main ##########################
pathex=[
  main_dir,
  path.join(main_dir, "filesystem"),
  path.join(main_dir, "dojo"),
  path.join(main_dir, "annotator"),
  path.join(main_dir, "gui"),
  path.join(main_dir, "plugins"),
  path.join(main_dir, "segment")
]

for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "plugins") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "plugins", dirpath))

for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "annotator") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

datas=[
          ( '../annotator/menu.json', './annotator/' ),
          ( '../plugins/menu.json', './plugins/' ),
          ( '../icons/*', './icons/' ),
          ( '../icons/Disabled/*', './icons/Disabled/' ),
          ( '../segment/menu.json', './segment/' )
      ]

hiddenimports=['scipy._lib.messagestream',
               'pywt._extensions._cwt',
               'PyQt5.sip',
               'numpy.core._dtype_ctypes',
               'gast'
              ]

#excludes=['PyQt5.QtQuick']


coll += analysis(['./../main.py'], pathex, datas, hiddenimports, 'main')



########################## train ##########################
pathex=[]
for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment","_3D_FFN","ffn") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

translate=[path.join(main_dir, "segment","_3D_FFN","ffn","train.py")]
hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','gast','astor','termcolor','google.protobuf.wrappers_pb2','tensorflow.contrib']

coll += analysis(translate, pathex, [], hiddenimports, 'train')



########################## run_inference_win ##########################
pathex=[]
for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment","_3D_FFN","ffn") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

translate=[path.join(main_dir, "segment","_3D_FFN","ffn","run_inference_win.py")]
hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','PyQt5.sip','gast','astor','termcolor','google.protobuf.wrappers_pb2','tensorflow.contrib']

coll += analysis(translate, pathex, [], hiddenimports, 'run_inference_win')



########################## build_coordinates ##########################
pathex=[]
for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment","_3D_FFN","ffn") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

translate=[path.join(main_dir, "segment","_3D_FFN","ffn","build_coordinates.py")]
hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','tensorflow.contrib']

coll += analysis(translate, pathex, [], hiddenimports, 'build_coordinates')



########################## compute_partitions ##########################
pathex=[]
for dirpath, dirnames, filenames in os.walk( path.join(main_dir, "segment","_3D_FFN","ffn") ):
    if os.path.basename(dirpath) != '__pycache__':
            pathex.append(path.join(main_dir, "segment", dirpath))

translate=[path.join(main_dir, "segment","_3D_FFN","ffn","compute_partitions.py")]
hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','tensorflow.contrib']

coll += analysis(translate, pathex, [], hiddenimports, 'compute_partitions')



########################## tensorboard ##########################
import tensorboard as _
WEBFILES = os.path.join(_.__path__[0], "webfiles.zip")

tensorb=[path.join(main_dir, "segment","_tensorb","launch_tensorboard.py")]
pathex=[]

datas=[ ( WEBFILES, './tensorboard/' ) ]
hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','tensorflow.contrib']

coll += analysis(tensorb, pathex, datas, hiddenimports, 'launch_tensorbord')



########################## translate ##########################
pathex=[path.join(main_dir, "segment","_2D_DNN")]
translate=[path.join(main_dir, "segment","_2D_DNN","translate.py")]

hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt','tensorflow.contrib']

coll += analysis(translate, pathex, [], hiddenimports, 'translate')



########################## Template ##########################
pathex=[path.join(main_dir, "plugin","Template")]
Template=[path.join(main_dir, "plugin","Template","Template.py")]

hiddenimports=['pywt._extensions._cwt']

coll += analysis(Template, pathex, [], hiddenimports, 'Template')


######### All Collect #########
print('### Collect All resources ###')
coll_all = COLLECT(*coll, strip=False, upx=True, name='main')
