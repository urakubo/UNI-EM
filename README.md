[Japanese version here](README.ja.md)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This software is under development!

# A unified environment for DNN-based automated segmentation of neuronal EM images

### table of contents
- [Introduction](#Introduction)
- [System requirements](#System-requirements)
- [Installation](#Installation)
- [Authors](#Authors)
- [License](#License)
- [Acknowledgments](#Acknowledgments)

---
Check the following pages after installation.
- [How to use: Dojo proofreader](Documents/HowToUse.md#Dojo-proofreader)
- [How to use: 3D annotator](Documents/HowToUse.md#3D-annotator)
- [How to use: 2D CNN](Documents/HowToUse.md#2D-CNN)
- [How to use: 3D FFN](Documents/HowToUse.md#3D-FFN)
- [How to use: 2D and 3D filters](Documents/HowToUse.md#2D-and-3D-filters)
- [Example workflow1: Mitochondria segmentation using 2D CNN](Documents/Workflow1.md)
- [Example workflow2: Membrane segmentation using 3D FFN](Documents/Workflow2.md) 
- [How to make a plugin](Documents/HowToMakePlugin.md) 
---

## Introduction
Recent years have seen a rapid expansion in the field of micro-connectomics, which targets 3D reconstruction of neuronal networks from a stack of 2D electron microscopic (EM). The spatial scale of the 3D reconstruction grows rapidly over 1 mm3, thank to deep neural networks (DNN) that enable automated neuronal segmentation. Advanced research teams have developed their own pipelines for the DNN-based large-scale segmentation (Informatics 2017, 4:3, 29). Those pipelines are typically a series of client-server software for alignment, segmentation, proofreading, etc., each of which requires specific PC configuration. Because of such complexity, it is difficult even for computer experts to use them, and impossible for experimentalists. This makes a serious divide between the advanced and general experimental laboratories.
   To bridge this divide, we are now trying to unify pieces of software for automated EM segmentation.

1.	We built a desktop version of the proofreading software Dojo (IEEE Trans. Vis. Comput. Graph. 20, 2466–2475) on Microsoft Windows 10, 64 bit.
2.	We merged it with a DNN framework: Google Tensorflow/tensorboard. 
3.	We then incorporated four types of DNN-based segmentation programs: 2D U-Net, ResNet, DenseNet, and HighwayNet. (https://github.com/tbullmann/imagetranslation-tensorflow) and flood-filling networks (https://github.com/google/ffn).
4.	A 3D annotator was equipped for visual inspection and annotation (based on Three.js).
5.	2D/3D filtration functions were equipped for pre/postprocessing of the segmented images (based on skimage and opencv3).

Multiple users can simultaneously use it through web browsers. The goal is to develop a unified software environment for DNN-based segmentation, ground truth segmentation, pre/postprocessing, proofreading, annotation, and visualization. The VAST Lite is recommended for 3D ground truth generation (https://software.rc.fas.harvard.edu/lichtman/vast/ ).

## System requirements
Operating system: Microsoft Windows 10 (64 bit). Linux and macOS versions will be built in future.
Recommendation: High-performance NVIDIA graphics card such as GeForce GTX 1080ti.

## Installation
We provide standalone versions (pyinstaller version) and Python source codes.

### Pyinstaller version 
1.	Download one of the following two versions, and unzip it:
	- CPU version (Ver0.70; 371 MB): https://www.dropbox.com/s/1jc9uh9bt7radnd/UNI-EM0.7_Pyinstaller_Light.zip?dl=0
	- CPU version (Ver0.71; 280 MB): https://www.dropbox.com/s/9ffnhko5ov7v02u/UNI-EM0.71_Pyinstaller.zip?dl=0 (Not yet validated)
   	- GPU version (Ver0.71: 936 MB): https://www.dropbox.com/s/p2azjpeks7isv73/UNI_EM0.71_GPU%20.zip?dl=0

	The GPU version can be used if the PC-equipped NVIDIA GPU has over 3.5 compute capability:

	- https://developer.nvidia.com/cuda-gpus

2.	Download sample EM/segmentation dojo files from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

3.	Please click the link "main.exe" in [UNI-EM] to launch the control panel.

4.	Select Dojo → Open Dojo Folder from the dropdown menu, and specify the folder of the sample EM/segmentation dojo files. Dojo will be launched as a web application.

### Python version 
1. Install Python 3.5 or 3.6 in a Microsoft Windows PC, 64 bit.
2. Install cuda 9.0 and cuDNN v7 for Tensorflow 1.12 (latest combination on 2018/12/20) if your PC has a NVIDIA-GPU.
3. Download the source codes from the github site:
   	- git clone https://github.com/urakubo/UNI-EM
4. Install the following modules of Python: Tensorflow-gpu, PyQt5, openCV3, pypng, tornado, pillow, libtiff, mahotas, h5py, lxml, numpy, scipy, scikit-image, pypiwin32, numpy-stl. Check also "requirements.txt". 
5. Copy [UNI-EM]/Marching_cube/marching_cubes.cp3X-win_amd64.pyd and paste it to {$INSTALL_PYTHON}\Lib\site-packages.

	- This marching cube program is obtained from the ilastik: https://github.com/ilastik/marching_cubes


6. Download sample EM/segmentation dojo files from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

7. Execute "python main.py" in the [UNI-EM] folder. The control panel will appear.

8.	Select Dojo → Open Dojo Folder from the dropdown menu, and specify the folder of the sample EM/segmentation dojo files. Dojo will be launched as a web application.

## Authors

* [**Hidetoshi Urakubo**](https://researchmap.jp/urakubo/?lang=english) - *Initial work* - 
* [**Ryoji Miyamoto**](https://polygonpla.net/) - *Frontend programming* - 
* [**Torsten Bullmann**](https://www.cb.hs-mittweida.de/en/mitarbeiterinnen-mitarbeiter-in-ihren-fachgruppen/bullmann-torsten.html) - *2D convolutional neural networks* -

## License

This project is licensed under the GNU General Public License (GPLv3) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
This software relies on the following excellent free yet copyrighted software packages. We obey policies of those software packages.

	- Flood-filling networks (Apache License 2.0)
	- Imagetranslation-tensorflow (MIT)
	- Tensorflow, Tensorboard (Apache License 2.0)
	- PyQT5 (GPLv3)
	- Rhoana Dojo (MIT)
	- Open CV3 (3-clause BSD License, https://opencv.org/license.html)
	- Scikit image (http://scikit-image.org/docs/dev/license.html)
	- Three.js (MIT)
	- Tabulator (MIT) https://github.com/olifolkerd/tabulator/blob/master/LICENSE
	- Bootstrap (MIT) https://getbootstrap.com/docs/4.0/about/license/

Hidetoshi Urakubo
2019/2/1
