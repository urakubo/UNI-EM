var ObjObjextTable = new Tabulator("#ObjectTable", {
	ajaxURL:"./data/segmentInfo.json",
	layout:"fitColumns",      //fit columns to width of table
	autoResize:true,
	responsiveLayout:"hide",  //hide columns that dont fit on the table
	tooltips:true,            //show tool tips on cells
	addRowPos:"top",          //when adding a new row, add it to the top of the table
	history:true,             //allow undo and redo actions on the table
	pagination:"local",       //paginate the data
	paginationSize:10,         //allow 7 rows per page of data
	resizableRows:true,       //allow row order to be changed
	initialSort:[             //set the initial sort order of the data
		{column:"name", dir:"asc"},
	],
	columns:[                 //define the table columns
    // ActやConfidenceはダウンロード時に除外されないよう定義しておく。ただしカラムvisible: falseにして非表示にする
    {title:"Act", field: "act", download: true, visible: false},
		{title:"Visible", field:"act", width: 73, align:"center",formatter:"tickCross", editor:"tickCross", download: false},
		{title:"ID", field:"id", width: 50},
		{title:"Name", field:"name", editor:"input"},
		{title:"Size", field:"size", width:60, align:"right"},
    {title:"Confidence", field: "confidence", download: true, visible: false},
		{title:"R", field:"r", minWidth: 30, width: 35, align:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"G", field:"g", minWidth: 30, width: 35, align:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"B", field:"b", minWidth: 30, width: 35, align:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
	],

	// セルが編集されたとき
  cellEdited: function(cell) {
      // 渡ってくるパラメータcellについて: http://tabulator.info/docs/4.1/components#component-cell
      // 編集後の値
      var cellValue = cell.getValue();
      // 編集前の値
      var cellOldValue = cell.getOldValue();
      // 編集対象のセルがある列
      var row = cell.getRow();
      var act = row.getData().act;
      var id  = row.getData().id;
      var r   = row.getData().r;
      var g   = row.getData().g;
      var b   = row.getData().b;
      // 編集したセルに対するカラムのフィールド
      var columnField = cell.getColumn().getField();
      // console.log("編集後の値:", cellValue, "編集前の値:", cellOldValue, "編集した列:", row, "編集したカラム", columnField);

	  if(columnField == 'act') {
	  	if(act == true) {
	  		console.log("Requested ID:", id );
	  		var host = location.hostname ;
	  		var port = location.port;
			call_url = "ws:"+host+":"+port+"/ws/display";
			filename = "http://"+host+":"+port+"/data/i%d.stl";
			var connection = new WebSocket(call_url);
			connection.onopen = function(){ connection.send(id); }
        	connection.onmessage = function (e) {
        		if(e.data == 'True') {
        			target_url = sprintf(filename, id );
        			console.log( target_url );
            		APP.addSTLObject(target_url, id, r*256*256+g*256+b*1);
            		};
				};
			}

	  	if(act == false) {
	  		console.log("Disappear ID:", id )
			filename = sprintf("./stls/i%d.stl", id );
			APP.removeSTLObject(id);
			}
		}

	  if(columnField == 'r' || columnField == 'g' || columnField == 'b') {
	  		console.log("Changecolor ID:", id )
			APP.changecolorSTLObject(id, r*256*256+g*256+b*1);
		}
    }

});

// 「Download CSV」ボタンを押したとき
$('#save-object-table-csv').on('click', function(event) {
  downloadObjectTableAsCSV();
  return false;
});

/**
 * ObjectTableをCSVでダウンロードする
 */
function downloadObjectTableAsCSV() {
  console.log("downloadObjectTableAsCSV");
  ObjObjextTable.download(csvFormatter, 'ObjextTable.csv');
}
