[English version here](HowToMakePlugin.md)

## 使い方：プラグインの作り方

UNI-EMでは、ご自身のPythonプログラムを容易にUNI-EMのプラグインにすることができます。ここでは、テンプレートプラグイン Templete がどのように導入されているか確認します。まず、UNI_EM\plugins\menu.json を開いて Plugin ドロップダウンメニューの内容を確認します。
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
ここで、最上位のkey (e.g., "2D/3D Filters") はPluginsのドロップダウンメニューの項目です。key "Sub" はドロップダウン階層を指定回数一段落とすことを示し、key "Func" は UNI_EM\plugins\Plugin.py にて呼び出される関数名を指定します。次に、UNI_EM\plugins\Plugin.py の内容を確認します。
```python
sys.path.append(path.join(plugins_dir, "Template"))
from Dialog_Template   import Dialog_Template

class Plugins():
    def Template(self):
        self.tmp = Dialog_Template(self)
```
一行目では UNI_EM\plugins\Template フォルダを参照することを指定し、二行目では Dialog_Template.py ファイルの Dialog_Templateクラスを読み込むことを指定し、def Template(self) 内で Dialog_Template を呼び出しています。さらに、UNI_EM\plugins\Template\Dialog_Template.pyを確認します。
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
最初の二行で Training.py および Inference.py 読み込み、initUI 内にて、Training tab と Inference tab を読み込みます。さらに、UNI_EM\plugins\Template\Training.py を確認します。
```python
##
exec_dir = os.path.join(main_dir, 'plugins','Template')
exec_train = 'python ' +  os.path.join(exec_dir, 'run_example.py')
##

class Training(MiscellaneousTemplate):
    def _Run(self, params, comm_title):
        ##
        comm_train = exec_train + ' ' \
                     + ' --training_image_folder '    + params['Training image folder'] + ' ' \
                     + ' --ground_truth_folder '      + params['Ground truth folder'] + ' ' \
                     + ' --tensorflow_model_folder ' + params['Tensorflow model folder']  + ' ' \
        s.run(comm_train.split())

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
exec_train にて実行する外部プログラムを指定します。


