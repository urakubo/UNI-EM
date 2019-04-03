プラグインの書き方

UNI-EMでは、ご自身のプログラムを容易にUNI-EMのプラグインとすることができます。まず、UNI_EM\plugins フォルダにおいて menu.json を開いて Plugin ドロップダウンメニューの内容を変更します。

{
"2D Filters": {
	"Sub":		0,
	"Func":		"_2D_Filters"
},
"3D Filters": {
	"Sub":		0,
	"Func":		"_3D_Filters"
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
"User Defined3": {
	"Sub":		0,
	"Func":		"UserDefined_"
}
}
