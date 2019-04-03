[Japanese version here](HowToMakePlugin.ja.md)

## How to make a plug-in
Users can easily embed their own executable programs (including python programs) in UNI-EM as a plug-in. Here we show how to make such a plug-in by introducing a pre-installed template. The template plug-in incorporates an external Python program "run_example.py" in UNI_EM\ plugins\Template. First, check the content of UNI_EM\plugins\menu.json that determines the Plugin dropdown menu.
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
Where the keys at a highest level (e.g., "2D/3D Filters") denote the contents of the dropdown menu, and the key "sub" denotes the numbers of lower-level contents that are generated afterwards. The keys "Func" denote the functions that are called in UNI_EM\plugins\Plugin.py. Here, Plugin.py is shown as follows: 

```python
sys.path.append(path.join(plugins_dir, "Template"))
from Dialog_Template   import Dialog_Template

class Plugins():
    def Template(self):
        self.tmp = Dialog_Template(self)
```
where the folder UNI_EM\plugins\Template is included in a search path (line 1), and Dialog_Template class in that folder is imported (line 2). The function "Template" assigns the Dialog_Template class to an object (line 6). Then, check the content of UNI_EM\plugins\Template\Dialog_Template.py. Dialog_Template.py is a program to generate the control panel (Widget) itself.
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
The program imports Training.py and Inference.py in the first two lines, and they are assigned to objects in initUI. Here UNI_EM\ plugins\Template\Training.py is show as follows:
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
                        ['Training image folder'   , 'LineEdit', training_image_path  , 'BrowseDirImg'],
                        ['Ground truth folder'     , 'LineEdit', ground_truth_path   , 'BrowseDirImg'],
                        ['Tensorflow model folder' , 'LineEdit', tensorflow_file_path  , 'BrowseDir'],
            ]
```
where the global variable exec_template holds the name of the target external program. Here, 
exec_template="python UNI_EM\plugins\Template\ run_example.py" In the function _Run, its arguments are specified and the function is executed by s.run. The arguments are set through a control panel (GUI), and the contents of the GUI is determined by the variable self.arg. For example, in the first line, it generates QSpinBox for setting a parameter entitled "Checkpoint Interval" under min=100, max=100, and the default value=1800. Here, self.tips denotes the tool tips that appear when the cursor point is located at the titles. If the Training class is successfully read by the subsequent GenerateTabWidget, the control panel appears shown as below. Users can set parameters through this control panel, and execute it by pressing the execute button.

<BR>
<p align="center">
  <img src="Images/Template_Training.png" alt="Template dialog" width="800">
</p>
<BR>　

