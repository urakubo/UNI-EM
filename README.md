[Japanese version here](README.ja.md)

![System requirements](https://img.shields.io/badge/platform-win%2064,%20linux%2064-green.svg)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# A unified environment for DNN-based automated segmentation of neuronal EM images

### Table of contents
- [Introduction](#Introduction)
- [System requirements](#System-requirements)
- [Installation](#Installation)
- [Authors](#Authors)
- [Reference](#Reference)
- [License](#License)
- [Acknowledgments](#Acknowledgments)

---
Check the following pages after installation.
- [How to use: Folder manager](docs/HowToUse.md#Folder-manager)
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

Caution: currently, UNI-EM cannot run on the newest NVIDIA GPUs, such as A100 and RTX30X0. This is because UNI-EM is based on tensorflow1.X, while the newest GPUs are compatible with tensorflow2.X, but not tensorflow1.X. Please refer to the following website.

- https://www.pugetsystems.com/labs/hpc/How-To-Install-TensorFlow-1-15-for-NVIDIA-RTX30-GPUs-without-docker-or-CUDA-install-2005/
- https://developer.nvidia.com/blog/accelerating-tensorflow-on-a100-gpus/
- https://github.com/NVIDIA/tensorflow

## Installation
We provide standalone versions (pyinstaller version) and Python source codes.

### Pyinstaller version (Microsoft Windows 10 only)
1.	Download one of the following two versions, and unzip it:

- Version 0.90.4 (2021/05/31):
	- [CPU version (Ver0.90.4; 363MB)](https://bit.ly/3uwKHkB)
	- [GPU version (Ver0.90.4: 1,068 MB)](https://bit.ly/2QWfFFb)

- Release summary:
	- Bug fix.
		- Bug fix version of FFNs was used.
		- Tentative solution in “Cannot lock file” error in the inference of 2D CNN.
		- Safe launch of Tensorboard.
		- Abolish the use of mcube (caused an occasional error in launching).

2.	Download one of sample EM/segmentation dojo folders from the following link, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

3.	Click the link "main.exe" in [UNI-EM] to launch the control panel.

4.	Select Dojo → Open Dojo Folder from the dropdown menu, and specify the folder of the sample EM/segmentation dojo files.  The proofreading software Dojo will be launched.

### Python version 
1. Install Python 3.5-3.7 in a Microsoft Windows PC (64 bit) or Linux PC (Ubuntu 18.04 confirmed).
2. Install cuda 10.0 and cuDNN 7.4 for Tensorflow 1.14 if your PC has a NVIDIA-GPU.

	- https://www.tensorflow.org/install/source
	- https://www.tensorflow.org/install/source_windows

3. Download source code from the github site:

	- git clone https://github.com/urakubo/UNI-EM.git

4. Install the following modules of Python: Tensorflow-gpu, PyQt5, openCV3, pypng, tornado, pillow, libtiff, mahotas, h5py, lxml, numpy, scipy, scikit-image, pypiwin32, numpy-stl. Check "requirements-[os]-[cpu or gpu].txt". Users can install those module using the following command.

	- pip install -r requirements-[os]-[cpu or gpu].txt

5. Download one of sample EM/segmentation dojo folders from the following link, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

6. Execute "python main.py" in the [UNI-EM] folder. The control panel will appear.

7.	Select Dojo → Open Dojo Folder from the dropdown menu, and specify the sample EM/segmentation dojo folder. The proofreading software Dojo will be launched.

## Authors

* [**Hidetoshi Urakubo**](https://researchmap.jp/urakubo/?lang=english) - *Initial work* - 
* [**Ryoji Miyamoto**](https://polygonpla.net/) - *Frontend GUI* - 
* [**Torsten Bullmann**](https://www.cb.hs-mittweida.de/en/mitarbeiterinnen-mitarbeiter-in-ihren-fachgruppen/bullmann-torsten.html) - *2D convolutional neural networks* -
* [**Naoki Tamura**](https://github.com/tamutamu) - *Deployment using pyinstaller* - 
* [**Ryoya Kamikawa**](https://ryoka.in) - *GUI of classic image filters* - 

## Reference

Urakubo, H., Bullmann, T., Kubota, Y., Oba, S., Ishii, S., UNI-EM: An Environment for Deep Neural Network-Based Automated Segmentation of Neuronal Electron Microscopic Images.
[**Scientific Reports 9, 19413 (2019) doi:10.1038/s41598-019-55431-0**](https://www.nature.com/articles/s41598-019-55431-0)

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
