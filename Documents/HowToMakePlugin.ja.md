[English version here](HowToMakePlugin.md)

## プラグインの作り方

UNI-EMでは、ご自身のPython等の実行形式プログラムを容易にプラグインにすることができます。ここでは、テンプレートプラグイン Templete がどのように導入されているか確認します。まず、UNI_EM\plugins\menu.json を開いてください。menu.json は Plugin ドロップダウンメニューの内容を指定しており、次の様な内容になります（抜粋）。
```json
{
"2D/3D Filters": {
	"Sub":		0,
	"Func":		"Filters"
},
"Template": {
	"Sub":		0,
	"Func":		"Template"
},
"User Defined1": {
	"Sub":		1,
	"Func":		"UserDefined_"
},
"User Defined2": {
	"Sub":		0,
	"Func":		"UserDefined_"
},
}
```
ここで、最上位のkey (e.g., "2D/3D Filters") はPluginsのドロップダウンメニューの項目です。key "Sub" はドロップダウン階層を指定回数一段落とすことを指示し、key "Func" は UNI_EM\plugins\Plugin.py にて呼び出される関数名を指定します。次に、menu.json より呼び出される UNI_EM\plugins\Plugin.py の内容を確認します（抜粋）。
```python
sys.path.append(path.join(plugins_dir, "Template"))
from Dialog_Template   import Dialog_Template

class Plugins():
    def Template(self):
        self.tmp = Dialog_Template(self)
```
一行目では UNI_EM\plugins\Template フォルダを参照することを指定し、二行目では Dialog_Template.py ファイルの Dialog_Templateクラスを読み込むことを指定し、def Template(self) 内で実際に Dialog_Template を呼び出しています。さらに、このダイアログ本体を作成する UNI_EM\plugins\Template\Dialog_Template.pyを確認します（抜粋）。
```python
from Training   import Training
from Inference  import Inference

class Dialog_Template(QWidget, MiscellaneousTemplate):
    def initUI(self):
	# Training
        training        = Training(self.u_info)
        tab_training    = self.GenerateTabWidget(training)
        tabs.addTab(tab_training, 'Training')

        # Inferernce
        inference        = Inference(self.u_info)
        tab_inference    = self.GenerateTabWidget(inference)
        tabs.addTab(tab_inference, 'Inference')
```
最初の二行で Training.py および Inference.py 読み込み、initUI 内にて、Training tab と Inference tab を読み込んでいます。さらに、Trainingタブの内容を決定する UNI_EM\plugins\Template\Training.py を確認します（抜粋）。
```python
##
exec_dir = os.path.join(main_dir, 'plugins','Template')
exec_template = 'python ' +  os.path.join(exec_dir, 'run_example.py')
##

class Training(MiscellaneousTemplate):
    def _Run(self, params, comm_title):
        ##
        comm_run = exec_train + ' ' \
                     + ' --training_image_folder '    + params['Training image folder'] + ' ' \
                     + ' --ground_truth_folder '      + params['Ground truth folder'] + ' ' \
                     + ' --tensorflow_model_folder ' + params['Tensorflow model folder']  + ' ' \
        s.run(comm_run.split())

    def __init__(self, u_info):
    	##
        self.name = 'Training'
        self.tips = [
                        'Checkpoint Interval',
                        'Sparse Z',
                        'Mode',
                        'Input : Training image folder',
                        'Input : Ground truth folder',
                        'Input/Output: Tensorlflow Model Folder'
                        ]

        self.args = [
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['Sparse Z', 'CheckBox', False],
                        ['Mode', 'ComboBox', ['a','b','c']],
                        ['Training image folder'   , 'LineEdit', training_image_path   , 'BrowseDirImg'],
                        ['Ground truth folder'     , 'LineEdit', ground_truth_path     , 'BrowseDirImg'],
                        ['Tensorflow model folder' , 'LineEdit', tensorflow_file_path  , 'BrowseDir'],
            ]
```
変数 exec_template に実行する外部プログラムを指定しています。ここでは、UNI_EM\plugins\Template\ フォルダ内の python run_example.py を指定しています。関数 _Run では引数を指定をすると共に s.run にて関数を実行しています。引数の指定は、関数__init__ にてself.arg を指定することで、GUIにて行います。上段左より、項目"Checkpoint Interval"を作って下限100, 上限65535, 既定値1800のSpinboxを作成し、Spinboxを介して値を設定することを示します。self.tipsは各項目上にマウスカーソルを置くと現れる注意書きです。Trainingクラスを実行したのち、GenerateTabWidget関数がクラス変数を正しく解釈することができると、下のようなダイアログ（Control panel) が現れます。Control panelを通じて各種引数の設定を行うと共に、"Execute"ボタンによりプログラムを実行することができます。

<BR>
<p align="center">
  <img src="Images/Template_Training.png" alt="Template dialog" width="800">
</p>
<BR>　




