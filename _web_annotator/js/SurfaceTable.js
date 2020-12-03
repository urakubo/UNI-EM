import { APP } from "./APP";
import { csvFormatter } from "./csv";
import { updateMetricsOnPaintTable } from "./HandleBasement";
import * as Tabulator from "tabulator-tables";

export const SurfaceTable = new Tabulator("#SurfaceTable", {
	ajaxURL:"./surface/segmentInfo.json",
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
		{title:"Visible", field:"act", width: 73, hozAlign:"center",formatter:"tickCross", cellClick: (e, cell)=>{cell.setValue(!cell.getValue());}, download: false},
		{title:"ID", field:"id", width: 50},
		{title:"Name", field:"name", editor:"input"},
		{title:"Size", field:"size", width:60, hozAlign:"right"},
    {title:"Confidence", field: "confidence", download: true, visible: false},
		{title:"R", field:"r", minWidth: 30, width: 35, hozAlign:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"G", field:"g", minWidth: 30, width: 35, hozAlign:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"B", field:"b", minWidth: 30, width: 35, hozAlign:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
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


	  var col = r*256*256+g*256+b*1 ;
	  if(columnField == 'act') {
	  	if(act == true) {
	  		console.log("Requested ID:", id );
			APP.addSurfaceObject(id, col);
			APP.addSkeletonObject(id, col);
			APP.addSphereObject(id, col);
			}
	  	if(act == false) {
	  		console.log("Disappear ID:", id )
			//const filename = sprintf("./stls/i%d.stl", id );
			APP.removeSurfaceObject(id);
			APP.removeSkeletonObject(id);
			APP.removeSphereObject(id);
			}
			updateMetricsOnPaintTable();
		}
	  if(columnField == 'r' || columnField == 'g' || columnField == 'b') {
	  	console.log("Changecolor ID:", id )
		APP.changeSurfaceObjectColor(id, col);
		APP.changeSkeletonObjectColor(id, col);
		}
    }

});

// 「Download CSV」ボタンを押したとき
$('#save-object-table-csv').on('click', function(event) {
  downloadSurfaceTableAsCSV();
  return false;
});

/**
 * ObjectTableをCSVでダウンロードする
 */
function downloadSurfaceTableAsCSV() {
  console.log("downloadObjectTableAsCSV");
  SurfaceTable.download(csvFormatter, 'SurfaceTable.csv');
}
