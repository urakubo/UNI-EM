プラグインの書き方

UNI-EMでは、ご自身のプログラムを容易にUNI-EMのプラグインとすることができます。まず、UNI_EM\plugins\menu.json を開いて Plugin ドロップダウンメニューの内容を変更します。
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
ここで、最上位のkey (e.g., "2D/3D Filters") はPluginsのドロップダウンメニュー項目、key "Sub" は指定回数ドロップダウン階層を一段深め、key "Func" はUNI_EM\plugins\Plugin.py にて呼び出される関数名を指示します。次に、UNI_EM\plugins\Plugin.py にて
```python
sys.path.append(path.join(plugins_dir, "Template"))
from Dialog_Template   import Dialog_Template

class Plugins():
    def Template(self):
        self.tmp = Dialog_Template(self)
```
