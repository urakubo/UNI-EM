[Japanese version here](README.ja.md)

![System requirements](https://img.shields.io/badge/Platform-win%2064,%20linux%2064-green.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# A unified environment for DNN-based automated segmentation of neuronal EM images

### Table of contents
- [Introduction](#Introduction)
- [System requirements](#System-requirements)
- [Installation](#Installation)
- [Authors](#Authors)
- [License](#License)
- [Acknowledgments](#Acknowledgments)

---
Check the following pages after installation.
- [How to use: Folder management system](HowToUse.md#Folder-management-system)
- [How to use: Dojo proofreader](docs/HowToUse.md#Dojo-proofreader)
- [How to use: 3D annotator](docs/HowToUse.md#3D-annotator)
- [How to use: 2D CNN](docs/HowToUse.md#2D-CNN)
- [How to use: 3D FFN](docs/HowToUse.md#3D-FFN)
- [How to use: 2D and 3D filters](docs/HowToUse.md#2D-and-3D-filters)
- [Example workflow1: Mitochondria segmentation using 2D CNN](docs/Workflow1.md)
- [Example workflow2: Membrane segmentation using 3D FFN](docs/Workflow2.md) 
- [How to make a plugin](docs/HowToMakePlugin.md) 
---

## Introduction
Recent years have seen a rapid expansion in the field of micro-connectomics, which targets 3D reconstruction of neuronal networks from a stack of 2D electron microscopic (EM). The spatial scale of the 3D reconstruction grows rapidly over 1 mm3, thank to deep neural networks (DNN) that enable automated neuronal segmentation. Advanced research teams have developed their own pipelines for the DNN-based large-scale segmentation (Informatics 2017, 4:3, 29). Those pipelines are typically a series of client-server software for alignment, segmentation, proofreading, etc., each of which requires specific PC configuration. Because of such complexity, it is difficult even for computer experts to use them, and impossible for experimentalists. This makes a serious divide between the advanced and general experimental laboratories.
   To bridge this divide, we are now trying to unify pieces of software for automated EM segmentation.

1.	We built a desktop version of the proofreading software Dojo (IEEE Trans. Vis. Comput. Graph. 20, 2466–2475).
2.	We merged it with a DNN framework: Google Tensorflow/tensorboard. 
3.	We then incorporated four types of DNN-based segmentation programs: 2D U-Net, ResNet, DenseNet, and HighwayNet. (https://github.com/tbullmann/imagetranslation-tensorflow) and flood-filling networks (https://github.com/google/ffn).
4.	A 3D annotator was equipped for visual inspection and annotation.
5.	2D/3D filtration functions were equipped for pre/postprocessing of the segmented images.

Multiple users can simultaneously use it through web browsers. The goal is to develop a unified software environment for  ground truth preparation, DNN-based segmentation, pre/postprocessing, proofreading, annotation, and visualization. 

## System requirements
Operating system: Microsoft Windows 10 (64 bit) or Linux (Ubuntu 18.04).

Recommendation: High-performance NVIDIA graphics card whose GPU has over 3.5 compute capability.

- https://developer.nvidia.com/cuda-gpus


## Installation
We provide standalone versions (pyinstaller version) and Python source codes.

### Pyinstaller version (Microsoft Windows 10 Only)
1.	Download one of the following two versions, and unzip it:

	- [CPU version (Ver0.78; 290 MB)](http://bit.ly/2IwquWk)
	- [GPU version (Ver0.78: 715 MB)](http://bit.ly/2wNKm1G)


	**Ver0.78 is the last release of this line. We will soon release the new version with a new feature "folder manager".**

2.	Download sample EM/segmentation dojo files from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

3.	Please click the link "main.exe" in [UNI-EM] to launch the control panel.

4.	Select Dojo → Open Dojo Folder from the dropdown menu, and specify the folder of the sample EM/segmentation dojo files.  The proofreading software Dojo will be launched.

### Python version 
1. Install Python 3.5 or 3.6 in a Microsoft Windows PC (64 bit) or Linux PC (Ubuntu 18.04 confirmed).
2. Install cuda 9.0 and cuDNN 7.4.2 (or later) for Tensorflow 1.12 (latest combination on 2018/12/20) if your PC has a NVIDIA-GPU.
3. Download the source codes from the github site:
   	- git clone https://github.com/urakubo/UNI-EM
4. Install the following modules of Python: Tensorflow-gpu, PyQt5, openCV3, pypng, tornado, pillow, libtiff, mahotas, h5py, lxml, numpy, scipy, scikit-image, pypiwin32, numpy-stl. Check also "requirements-[os]-[cpu or gpu].txt". 
5. **Copy [UNI-EM]\marching_cubes\marching_cubes`*` and paste it to {$INSTALL_PYTHON}\Lib\site-packages.**

	- **Execute the Python command "import site; site.getsitepackages()" to find {$INSTALL_PYTHON}.**
	
	
	The marching cube program is obtained from the ilastik: https://github.com/ilastik/marching_cubes


6. Download sample EM/segmentation dojo files from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

7. Execute "python main.py" in the [UNI-EM] folder. The control panel will appear.

8.	Select Dojo → Open Dojo Folder from the dropdown menu, and specify the folder of the sample EM/segmentation dojo files. The proofreading software Dojo will be launched.

## Authors

* [**Hidetoshi Urakubo**](https://researchmap.jp/urakubo/?lang=english) - *Initial work* - 
* [**Ryoji Miyamoto**](https://polygonpla.net/) - *Frontend GUI* - 
* [**Torsten Bullmann**](https://www.cb.hs-mittweida.de/en/mitarbeiterinnen-mitarbeiter-in-ihren-fachgruppen/bullmann-torsten.html) - *2D convolutional neural networks* -
* [**Naoki Tamura**](https://github.com/tamutamu) - *Deployment using pyinstaller* - 
* [**Ryoya Kamikawa**](https://ryoka.in) - *GUI of classic image filters* - 


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
