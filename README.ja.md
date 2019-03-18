[English version here](README.md)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# DNNを用いた神経EM画像セグメンテーションのための統合環境（UNI-EM）

### 目次
- [はじめに](#はじめに)
- [動作条件](#動作条件)
- [インストール方法](#インストール方法)
- [お願い](#お願い)

---
インストール後は下のページを参照してください。
- [使い方：校正ソフトウェアDojo](Documents/HowToUse.ja.md#校正ソフトウェアDojo)
- [使い方：3D Annotator](Documents/HowToUse.ja.md#3D-Annotator)
- [使い方：2次元DNNを用いたセグメンテーション](Documents/HowToUse.ja.md#2次元DNNを用いたセグメンテーション)
- [使い方：3次元FFNを用いたセグメンテーション](Documents/HowToUse.ja.md#3次元FFNを用いたセグメンテーション)
- [使い方：2D/3Dフィルタ](Documents/HowToUse.ja.md#2D3Dフィルタ)
- [適用事例1：2次元DNNによるミトコンドリアのセグメンテーション](Documents/Workflow1.ja.md)
- [適用事例2：3次元FFNによる細胞膜のセグメンテーション](Documents/Workflow2.ja.md)
---

## はじめに：
近年、コネクトミクス（コネクトーム）呼ばれる脳神経の大規模解剖学が注目を浴びています。特に、電子顕微鏡（EM）に基づいて神経回路の具体的な配線図を明らかにするミクロコネクトミクスはその代表的なものです。ミクロコネクトミクスのためには電子顕微鏡(EM; ATUM SEM / SBF SEM / FIB SEM）により撮影された三次元神経画像（二次元画像のスタック）が必要ですが、さらに二次元画像間の位置合わせ（レジストレーション）・深層学習による細胞膜分割（セグメンテーション）・人手による校正（プルーフリード）・情報のタグ付け（アノテーション）などの情報処理が必要になります。

　このような神経EM画像処理のためのソフトウェアは、Janelia research campus, Princeton大学, Harvard大学などアメリカはじめ、いくつかの研究機関において開発が進められています。複数のソフトウェアを連結して利用するためパイプラインと呼ばれます。ただし、これらパイプラインは各々独自のファイルフォーマットを採用していたり、複雑な設定が必要なサーバ・クライアントシステムであったりするなど、基本的にコンピュータエキスパートが利用することを前提としています。実験研究者が利用することは非常に困難です。

　そこで、私たちはパイプライン上のソフトウェアのいくつかを実験研究者にも簡単に使えるように統合する作業を始めました。

* まずHarvard 大学、Lichtman 研が開発した Rhoana パイプラインのDojoという校正ソフトウェア（サーバ＆クライアントシステム）に注目し、原作者(Daniel Haehn)の許可のもと改変してWindows　PCデスクトップアプリとしました **[改装・改良中 18/12/17]** 。
* さらに、同アプリに深層学習の基盤ソフトウェアであるTensorflow/ Tensorboard (Google) および深層学習に基づいた二種類のセグメンテーションソフトウェア"2D DNN (Resnetほか)", "3D FFN" を統合しました。
* セグメンテーション結果を3Dで確認・アノテーションすることができるようにするために、3D annotatorを作成しました。
* 推定画像の操作を行うために2D/3D フィルタを作成しました。

深層学習のプログラム知識を持たない実験研究者が、EM画像/教師セグメンテーションをもとに「DNNによるセグメンテーション」「各種フィルタ処理」「人手による校正（プルーフリード）・アノテーション」「視覚化」までできるようにすることを目標とします。教師セグメンテーションの作成にはVast liteの使用をお勧めします ( https://software.rc.fas.harvard.edu/lichtman/vast/ ) 。


## 動作条件：
OSはMicrosoft Windows 10 (64 bit) です。メインメモリ8GB以上のPCで動きます。深層学習を行う場合は、NVIDIA社のグラフィックスカードを搭載したPCを使用することを推奨します。GeForce GTX 1080tiなどの高性能なGPUを搭載したグラフィックスカードの使用を推奨します。ユーザの希望がありましたらLinuxやmacOSに移植します。

## インストール方法：
Pythonのインストールの必要のないPyinstaller版とPythonソースコードの両方を提供します。

### Pyinstaller版：
1. Tensorflow-GPU 版(498 MB)とTensorflow-CPU版(XXX MB, 作成中)を用意しました。いずれかをダウンロードして展開してください。
	- CPU版 (340 MB; Ver 0.62): https://www.dropbox.com/s/a8aepoikrpsmgob/UNI_EM0.62_Pyinstaller.zip?dl=0
	
	- GPU版 (Ver0.62: XXX MB): Under construction.

2. 公開サンプルデータkasthuri15をダウンロードして適当なフォルダに展開してください。
	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

3. Dojo_StandaloneX.XXフォルダ中のmain.exeをクリックして、コントロールパネルを起動してください。

4. 上端のドロップダウンメニューより一番左のDojo → Open Dojo Folderを選択して、ダイアログよりkasthuri15フォルダ下のmojoを指定してください。サンプルデータがダウンロードされてDojoが起動します。

### Python版：
1. Windows10 において、 Python3.5-3.6 をインストールしてください。
2. Tensorflow 1.12 のためにGPUを利用する場合はcuda 9.0, cuDNN v7をインスト―ルしてください **[参考1]** 。
3. 次の命令を実行してGithubより必要プログラムをダウンロードしてください。
	 - git clone https://github.com/urakubo/Dojo-standalone
4. requirements.txtを参考、Pythonに必要モジュール「Tensorflow-gpu 1.12, PyQt5, openCV3, pypng, tornado, pillow, libtiff, mahotas, h5py, lxml, numpy, scipy, scikit-image, pypiwin32, numpy-stl」を にpip install -r requirements.txt (あるいはconda）などのコマンドを用いてインストールしてください。
5. Dojo_StandaloneX.XX/Marching_cube/marching_cubes.cp3X-win_amd64.pyd を {$INSTALL_PYTHON}\Lib\site-packages へコピーしてください。{$INSTALL_PYTHON} は例えばAnacondaであれば、conda info -e コマンドにより分かります。
6. コマンドププロンプトにてDojo_StandaloneX.XXフォルダへ移動して、 python main.py と実行してコントロールパネルを起動してください。
7. 公開サンプルデータkasthuri15をダウンロードして適当なフォルダに展開してください。
	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

8. 上端のドロップダウンメニューより一番左のDojo → Open Dojo Folderを選択して、ダイアログよりkasthuri15フォルダ下のmojoを指定してください。サンプルデータがダウンロードされてDojoが起動します。

## お願い：
2019/2/11現在、まだ実用では使われていません。しかし、日本国内の実験研究者、情報学研究者さまのフィードバックをお待ちします（urakubo-h あっと sys.i.kyoto-u.ac.jp; **[参考3]** ）。私一人で開発を続けることは困難なので、共同開発者も募集いたします。本アプリは、自然画像のセグメンテーション等に利用することも可能と思われますので、多様なコメントをお待ちしております。本アプリの開発には、革新脳、新学術、基盤Cのご支援をいただいております。

- (参考1) cuda 9.0, cuDNN v7のインストール方法。
	- <https://qiita.com/spiderx_jp/items/8d863b087507cd4a56b0>
	- <https://qiita.com/kattoyoshi/items/494238793824f25fa489>
	- <https://haitenaipants.hatenablog.com/entry/2018/07/25/002118>

- (参考2) さらに詳細なマニュアル設定を行ってtrainingを実行したい場合は、Python スクリプトを作成したのち、コントロールパネル上端のプルダウンメニューよりScript → Run Scriptを選択して実行してください（実装中です。書き方も記述します）。およびTorsten Bullmann博士のGithubサイトを参照してください。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>

- (参考3) 浦久保 個人情報サイト。
	- <https://researchmap.jp/urakubo/>
