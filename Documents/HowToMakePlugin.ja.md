プラグインの書き方

UNI-EMでは、ご自身のプログラムを容易にUNI-EMのプラグインとすることができます。まず、UNI_EM\plugins フォルダにおいて menu.json を開いて Plugin ドロップダウンメニューの内容を変更します。
```json
{
"2D/3D Filters": {
	"Sub":		0,
	"Func":		"_2D_Filters"
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
