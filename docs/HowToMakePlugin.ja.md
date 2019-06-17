[English version here](HowToMakePlugin.md)

## プラグインの作り方

UNI-EMでは、ご自身のPython等の実行形式プログラムを容易にプラグインにすることができます。ここでは、Templateプラグインがどのように導入されるか確認します。ここで、Template プラグインにて実行されるPythonプログラムは UNI_EM\plugins\Template\run_example.py です。まず、UNI_EM\plugins\menu.json を開いてください。menu.json は Plugin ドロップダウンメニューの内容を指定しており、次の様な内容になります（抜粋）。
```json
{
"2D/3D Filters": {
	"Sub":		0,
	"Func":		"Filters2D3D"
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
ここで、最上位のkey (e.g., "2D/3D Filters") はPluginsのドロップダウンメニューの項目です。key "Sub" はドロップダウン階層を指定回数一段落とすことを指示し、key "Func" では、たとえばTemplateがクリックされると関数 UNI_EM\plugins\Template\Template.py を呼び出されることを示します。そこで、UNI_EM\plugins\Template\Dialog_Template.pyを確認します（抜粋）。Dialog_Template.py では、GenerateDialog class が自動的に呼びだされ、Control panel (Widget)本体が作成されます。
```python
from Template.Training   import Training
from Template.Inference  import Inference

class GenerateDialog(QWidget, MiscellaneousTemplate):
    def __init__(self, parent):
        self.title  = "Template"
	...
        self.initUI()

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
最初の二行で Training.py および Inference.py 読み込み、initUI 内にて、Training tab と Inference tab を読み込んでいます。さらに Trainingタブの内容を決定する UNI_EM\plugins\Template\Training.py を確認します（抜粋）。
```python
##
exec_dir = os.path.join(main_dir, 'plugins','Template')
exec_template = 'python ' + os.path.join(exec_dir, 'run_example.py')
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
                        'Input : Training image folder',
                        'Input : Ground truth folder',
                        'Input/Output: Tensorlflow Model Folder',
                        'Checkpoint Interval',
                        'Sparse Z',
                        'Mode'
                        ]

        self.args = [
                        ['Training image folder', 'SelectImageFolder', 'OpenImageFolder'],
                        ['Ground truth folder', 'SelectImageFolder', 'OpenImageFolder'],
                        ['Tensorflow model folder', 'LineEdit', tensorflow_path, 'BrowseDir'],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['Sparse Z', 'CheckBox', False],
                        ['Mode', 'ComboBox', ['a','b','c']]
            ]
```
変数 exec_template に実行する外部プログラムを指定しています。ここで UNI_EM\plugins\Template\ フォルダ内の python run_example.py を指定しています。関数 _Run では引数を指定をすると共に s.run にて関数を実行しています。引数の指定は、関数__init__ にてself.arg を指定することを介して GUIにて行います。上段左より、項目"Checkpoint Interval"を作って下限100, 上限65535, 既定値1800のSpinboxを作成し、Spinboxを介して値を設定するように指示します。self.tipsは各項目上にマウスカーソルを置くと現れる注意書きです。Trainingクラスを実行したのち、GenerateTabWidget関数がクラス変数を正しく解釈することに成功すると、下のようなControl panel (Widget) が現れます。Control panelを通じて各種引数の設定を行うと共に、"Execute"ボタンによりプログラムを実行することができます。

<BR>
<p align="center">
  <img src="Images/Template_Training.png" alt="Template dialog" width="800">
</p>
<BR>　




