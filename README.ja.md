[English version here](README.md)

![System requirements](https://img.shields.io/badge/platform-win%2064,%20linux%2064-green.svg)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# DNNを用いた神経EM画像セグメンテーションのための統合環境（UNI-EM）

### 目次
- [はじめに](#はじめに)
- [動作条件](#動作条件)
- [インストール方法](#インストール方法)
- [お願い](#お願い)

---
インストール後は下のページを参照してください。

- [使い方：フォルダ管理システム](docs/HowToUse.ja.md#フォルダ管理システム)
- [使い方：校正ソフトウェアDojo](docs/HowToUse.ja.md#校正ソフトウェアDojo)
- [使い方：3D Annotator](docs/HowToUse.ja.md#3D-Annotator)
- [使い方：2次元DNNを用いたセグメンテーション](docs/HowToUse.ja.md#2次元DNNを用いたセグメンテーション)
- [使い方：3次元FFNを用いたセグメンテーション](docs/HowToUse.ja.md#3次元FFNを用いたセグメンテーション)
- [使い方：2D/3Dフィルタ](docs/HowToUse.ja.md#2D3Dフィルタ)
- [適用事例1：2次元DNNによるミトコンドリアのセグメンテーション](docs/Workflow1.ja.md)
- [適用事例2：3次元FFNによる細胞膜のセグメンテーション](docs/Workflow2.ja.md)
- [プラグインの作り方](docs/HowToMakePlugin.ja.md) 
---

## はじめに：
近年、コネクトミクスと呼ばれる脳神経の大規模解剖学が注目を浴びています。特に、電子顕微鏡（EM）に基づいて神経回路の具体的な配線図（コネクトーム）を明らかにするミクロコネクトミクスはその代表的なものです。ミクロコネクトミクスのためには電子顕微鏡(EM; ATUM SEM / SBF SEM / FIB SEM）により撮影された三次元神経画像（二次元画像のスタック）が必要ですが、さらに二次元画像間の位置合わせ（レジストレーション）・深層学習による細胞膜分割（セグメンテーション）・人手による校正（プルーフリード）・情報のタグ付け（アノテーション）などの情報処理が必要になります。

　このような神経EM画像処理のためのソフトウェアは、Janelia research campus, Princeton大学, Harvard大学などアメリカはじめ、いくつかの研究機関において開発が進められています。複数のソフトウェアを連結して利用するためパイプラインと呼ばれます。ただし、これらパイプラインは各々独自のファイルフォーマットを採用していたり、複雑な設定が必要なサーバ・クライアントシステムであったりするなど、基本的にコンピュータエキスパートが利用することを前提としています。実験研究者が利用することは非常に困難です。

　そこで、私たちはパイプライン上のソフトウェアのいくつかを実験研究者にも簡単に使えるように統合する作業を始めました。

* まずHarvard 大学、Lichtman 研が開発した Rhoana パイプラインのDojoという校正ソフトウェア（サーバ＆クライアントシステム）に注目し、原作者(Daniel Haehn)の許可のもと改変してデスクトップアプリとしました。
* さらに、同アプリに深層学習の基盤ソフトウェアであるTensorflow/ Tensorboard (Google) および深層学習に基づいた二種類のセグメンテーションソフトウェア"2D DNN (Resnetほか)", "3D FFN" を統合しました。
* セグメンテーション結果を3Dで確認・アノテーションすることができるようにするために、3D annotatorを作成しました。
* 推定画像の操作を行うために2D/3D フィルタを作成しました。

深層学習のプログラム知識を持たない実験研究者が、EM画像をもとに「教師セグメンテーションの作成」「DNNによるセグメンテーション」「各種フィルタ処理」「人手による校正（プルーフリード）・アノテーション」「視覚化」までできるようにすることを目標とします。


## 動作条件：
OS：　Microsoft Windows 10 (64 bit) または Linux (Ubuntu 18.04にて動作確認済) 

推奨：NVIDIA社の高性能GPUを搭載したグラフィックスカード (Compute capability 3.5 以上のGPU搭載のもの。GeForce GTX1080ti, RTX2080ti, RTX3090など)。

- https://developer.nvidia.com/cuda-gpus

## インストール方法：
Pythonのインストールの必要のないPyinstaller版とPythonソースコードの両方を提供します。

### Pyinstaller版 (Windows10のみ)：
1. GPU 版とCPU版を用意しました。いずれかをダウンロードして展開してください。

- Version 0.92 (2021/09/13):
	- [CPU & GPU version (Ver0.92; XXX MB)](https://bit.ly/3uwKHkB)

- 前Version 0.90.4 (2021/05/31):
	- [CPU version (Ver0.90.4; 363MB)](https://bit.ly/3uwKHkB)
	- [GPU version (Ver0.90.4: 1,068 MB)](https://bit.ly/2QWfFFb)

2. 公開サンプルデータkasthuri15をダウンロードして適当なフォルダに展開してください。
	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

3. UNI-EMフォルダ中のmain.exeをクリックして、コントロールパネルを起動してください。

4. 上端のドロップダウンメニューより一番左のDojo → Open Dojo Folderを選択して、ダイアログよりkasthuri15フォルダ下のmojoを指定してください。サンプルデータがダウンロードされてDojoが起動します。

### Python版：
1. Windows10またはLinux (Ubuntu18.04 にて動作確認済)にて Python3.6- をインストールしてください。
2. Tensorflow 1.15, Tensorflow2.0- にて動作します。 NVIDIA GPU 利用する場合、Tensorflow 2.4.1の場合は"CUDA 11.0, cuDNN 8.0.4", TensorFlow 2.5.0の場合は"CUDA 11.2.2, cuDNN 8.1.1"をインスト―ルしてください **[参考1]** 。
3. 次の命令を実行してGithubより必要プログラムをダウンロードしてください。

	- git clone https://github.com/urakubo/UNI-EM.git


4. requirements-[os].txtを参考に、Pythonに必要モジュールを pip install -r requirements-[os].txt などのコマンドによりインストールしてください。Ubuntu18.04, Ubuntu20.04の場合は、 opencv, pyqt5 は apt でインストールしてください。

	- sudo apt install python3-dev python3-pip
	- sudo apt install python3-opencv
	- sudo apt install python3-pyqt5
	- sudo apt install python3-pyqt5.qtwebengine

5. コマンドププロンプトにて[UNI-EM]フォルダへ移動して、 python main.py と実行してコントロールパネルを起動してください。
6. 公開サンプルデータkasthuri15をダウンロードして適当なフォルダに展開してください。
	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

7. 上端のドロップダウンメニューより一番左のDojo → Open Dojo Folderを選択して、ダイアログよりkasthuri15フォルダ下のmojoを指定してください。サンプルデータがダウンロードされてDojoが起動します。

## お願い：
日本国内の実験研究者、情報学研究者さまのフィードバックをお待ちします（hurakubo あっと gmail.com; **[参考3]** ）。私一人で開発を続けることは困難なので、共同開発者も募集いたします。本アプリは、自然画像のセグメンテーション等に利用することも可能と思われますので、多様なコメントをお待ちしております。本アプリの開発には、革新脳、新学術、基盤Cのご支援をいただいております。

- (参考1) cuda 10.0, cuDNN v7.4のインストール方法。
	- <https://www.kkaneko.jp/tools/win/tensorflow114.html>
	- <https://www.tensorflow.org/install/source_windows?hl=ja>
	- <https://www.tensorflow.org/install/source?hl=ja>

- (参考2) さらに詳細なマニュアル設定を行ってtrainingを実行したい場合は、Python スクリプトを作成したのち、コントロールパネル上端のプルダウンメニューよりScript → Run Scriptを選択して実行してください（実装中です。書き方も記述します）。およびTorsten Bullmann博士のGithubサイトを参照してください。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>

- (参考3) 浦久保 個人情報サイト。
	- <https://researchmap.jp/urakubo/>
