import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import * as Tabulator from "tabulator-tables";

export const MarkerTable = new Tabulator("#MarkerTable", {
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
		{column:"id", dir:"dsc"},
	],
	columns:[                 //define the table columns
    // ActやX,Y,Zはダウンロード時に除外されないよう定義しておく。ただしカラムvisible: falseにして非表示にする
    {title:"Act", field: "act", download: true, visible: false},
		{title:"Delete", formatter:"buttonCross", width: 73, hozAlign:"center", editor:"tickCross", editable: onDeleteCheck, download: false},
		{title:"ID", field:"id", width: 40},

    // マーカー名を入力する時に日本語などASCII外が入力されないようにする
    // 入力されるとCSVファイルダウンロード→インポートを通して文字化けが発生するため、[ a-zA-Z0-9_-] のみ使用可能とする
		{title:"Name", field:"name", width: 70, editor:"input", validator: function(cell, value, parameters) {
      return util.isMarkerName(value);
    }},

		{title:"Parent ID", field:"parentid", width: 70},
		{title:"Radius", field:"radius", width: 60, hozAlign:"right", editor:"number",editorParams:{min:0.01, max:1, step:0.01}},
		{title:"R", field:"r", minWidth: 30, width: 35, hozAlign:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"G", field:"g", minWidth: 30, width: 35, hozAlign:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"B", field:"b", minWidth: 30, width: 35, hozAlign:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
    {title:"X", field:"x", download: true, visible: false},
    {title:"Y", field:"y", download: true, visible: false},
    {title:"Z", field:"z", download: true, visible: false}
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
    var radius  = row.getData().radius;
    var r   = row.getData().r;
    var g   = row.getData().g;
    var b   = row.getData().b;
    var columnField = cell.getColumn().getField();

    if (columnField == 'radius') {
      APP.changeMarkerRadius(id, radius);
    }

    if (columnField == 'r' || columnField == 'g' || columnField == 'b') {
      APP.changeMarkerColor(id, r*256*256+g*256+b*1);
    }
   }
});


// 「Import CSV」ボタンを押したとき
$('#import-csv-marker-table').on('change', onImportCSVFileSelect);

// 「Clear」ボタンを押したら3Dマーカーをクリアする
$('#clear-marker-table').on('click', function(event) {
  clearMarkerTable();
  return false;
});

// 「Download CSV」ボタンを押したとき
$('#save-marker-table-csv').on('click', function(event) {
  downloadMarkerTableAsCSV();
  return false;
});


// Deleteのチェックが押されたとき
function onDeleteCheck(cell) {
  var data = cell.getRow().getData();
  APP.removeMarker(data.id);
  cell.getRow().delete();
}

// 「Import CSV」ボタンが押されてファイルを選択したとき
function onImportCSVFileSelect(event) {
  var file = event.originalEvent.target.files[0];

  var reader = new FileReader();
  reader.onload = function(e) {
    var csvFileContent = e.target.result;
    var parsedData = parseCSV(csvFileContent);

    // 1行目のタイトルを除外
    parsedData.shift();
    // タイトルフィールドを変換
    var markers = replaceColumnTitle(MarkerTable, parsedData);

    // 同じ座標のためスキップした数
    var sameCoordinatesCount = 0;
    // Parent ID のオブジェクトが非表示のためスキップした数
    var parentNotVisibleCount = 0;

    markers.forEach(function(markerData) {
      if (!validateMarkerDataType(markerData)) {
        // 不正な値があったらスキップ
        console.error("Invalid marker data", markerData);
      } else if (!validateMarkerDataXYZ(markerData)) {
        // すでに同じ座標で定義済みだったらスキップ
        console.warn("Skipped: The loaded marker has been defined as same coordinates.", markerData);
        sameCoordinatesCount++;
      } else {
        var isAdded = APP.renderMarker(markerData);
        if (!isAdded) {
          // Parent ID のオブジェクトが非表示だったらエラーを出す
          console.warn("Skipped: The loaded marker's parent object has not visible.", markerData);
          parentNotVisibleCount++;
        }
      }
    });

    var errorMsg = [];
    if (sameCoordinatesCount) {
      errorMsg.push(sameCoordinatesCount + " Skipped: The loaded marker has been defined as same coordinates.");
    }
    if (parentNotVisibleCount) {
      errorMsg.push(parentNotVisibleCount + " Skipped: The loaded marker's parent object has not visible.");
    }
    if (errorMsg.length) {
      // スキップしたとき毎回アラートを出すとアラート数が増えすぎるのでまとめて通知する
      alert(errorMsg.join("\n"));
    }

    // 選択したファイル情報をクリア。これをしないと同じファイルを再度読み込めない
    $('#import-csv-marker-table').val('');
  };
  reader.readAsText(file);
}

/**
 * MarkerTableが空かどうか
 *
 * @return {bool}
 */
function isMarkerTableEmpty() {
  return MarkerTable.getDataCount() === 0;
}

/**
 * MarkerTableをクリアする
 */
function clearMarkerTable() {
  var rows = MarkerTable.getRows();
  rows.forEach(function(row) {
    APP.removeMarker(row.getData().id);
    row.delete();
  });
}

/**
 * MarkerTableをCSVでダウンロードする
 */
function downloadMarkerTableAsCSV() {
  MarkerTable.download(csvFormatter, 'MarkerTable.csv');
}

/**
 * テーブルカラムのタイトルとフィールドのペアを取得する
 *
 * @example
 * getColumnFieldTitlePairs(MarkerTable)
 * {
 *   "Act": "act"
 *   "ID": "id"
 *   "Name": "name"
 *   "Parent ID": "parentid"
 *   "Radius": "radius"
 *   "R": "r"
 *   "G": "g"
 *   "B": "b"
 *   "X": "x"
 *   "Y": "y"
 *   "Z": "z"
 * }
 */
function getColumnFieldTitlePairs(table) {
  var columnDefinitions = table.getColumnDefinitions();
  var fieldTitlePairs = {};
  columnDefinitions.forEach(function(column) {
    fieldTitlePairs[column.title] = column.field;
  });
  return fieldTitlePairs;
}

/**
 * キーがのタイトルのJSONデータをフィールド名にを変換する
 * CSVの1行目タイトルは表記用のものでスペースも含まれるため、内部キー名に変換する
 *
 * @example
 * replaceColumnTitle(MarkerTable, {
 *   "Act": "1"
 *   "ID": "2"
 *   "Name": "Marker1"
 *   "Parent ID": "3036"
 *   "Radius": "2"
 *   "R": "255"
 *   "G": "0",
 *   ...
 * });
 *
 * // 以下のようになる
 * {
 *   "act": "1"
 *   "id": "2"
 *   "name": "Marker1"
 *   "parentid": "3036"
 *   "radius": "2"
 *   "r": "255"
 *   "g": "0",
 *   ...
 * }
 */
function replaceColumnTitle(table, json) {
  var fieldTitlePairs = getColumnFieldTitlePairs(table);
  return json.reduce(function(memo, data) {
    var newData = {};
    Object.keys(data).forEach(function(key) {
      var value = data[key];
      var newKey = fieldTitlePairs[key];
      newData[newKey] = value;
    });
    memo.push(newData);
    return memo;
  }, []);
}


/**
 * renderMarkerに渡されるパラメータが適切な値かチェックする
 * CSVファイルから読まれ不正な値の可能性があるので扱える値かどうかを調べる
 *
 * @param  {Object} markerData renderMarkerの引数と同じ
 * @return {bool} すべての値が適切ならtrue,そうじゃないならfalse
 */
function validateMarkerDataType(markerData) {
  if (!util.isNumeric(markerData.act)) {
    return false;
  }
  if (!util.isNumeric(markerData.id)) {
    return false;
  }
  if (!util.isNumeric(markerData.parentid)) {
    return false;
  }
  if (!util.isNumeric(markerData.radius)) {
    return false;
  }
  if (!util.isNumeric(markerData.r)) {
    return false;
  }
  if (!util.isNumeric(markerData.g)) {
    return false;
  }
  if (!util.isNumeric(markerData.b)) {
    return false;
  }
  if (!util.isNumeric(markerData.x)) {
    return false;
  }
  if (!util.isNumeric(markerData.y)) {
    return false;
  }
  if (!util.isNumeric(markerData.z)) {
    return false;
  }
  if (!util.isMarkerName(markerData.name)) {
    return false;
  }
  return true;
}

/**
 * CSVファイルから読み込んだMarkerデータで、表示中のMarkerTableと同じ座標のものがあるかチェックする
 *
 * @param  {Object} markerData renderMarkerの引数と同じ
 * @return {bool} すべての値が適切ならtrue,そうじゃないならfalse
 */
function validateMarkerDataXYZ(markerData) {
  var rows = MarkerTable.getRows();
  return rows.every(function(row) {
    var rowData = row.getData();
    var rowX = rowData.x;
    var rowY = rowData.y;
    var rowZ = rowData.z;
    var markerDataX = Number(markerData.x);
    var markerDataY = Number(markerData.y);
    var markerDataZ = Number(markerData.z);

    // 浮動小数点数のため、小数点2桁までで比較する。だいたい同じ座標かどうかチェックする
    if (rowX.toFixed(2) === markerDataX.toFixed(2) &&
        rowY.toFixed(2) === markerDataY.toFixed(2) &&
        rowZ.toFixed(2) === markerDataZ.toFixed(2)) {
      // 同じ座標
      return false;
    }
    return true;
  });
}
