import { APP } from "./APP";
import { updatePaintObservation, paintManager } from "./SyncPaint";
import { setColorOptions } from "./three_annotator/index";
import * as Tabulator from "tabulator-tables";

const mutatorClip = (value, data, type, mutatorParams, component) => {
  const min = mutatorParams.min;
  const max = mutatorParams.max;
  return value <= min ? min :
         value >= max ? max :
         value;
}

const mutatorParamsClip = {min: 0, max: 255};

// 0-1までのなるべく離れた値を返す
const reversalBit = index => {
  let original = index, fraction = 1, value = 0;
  while(original) {
    const bit = original % 2;
    original = (original - bit) / 2;
    fraction /= 2;
    value += bit * fraction;
  }
  return value;
}

// 彩度が最大で、なるべく異なる色相の色を返す
const getRandomColor = (index) => {
  const value = ((reversalBit(index - 1)) % 1) * 3;
  const mainColorType = Math.floor(value);
  const subColorValue = Math.floor((value - mainColorType) * 255);
  const colors = [subColorValue, 255 - subColorValue];
  colors.splice(mainColorType, 0, 0);
  return {
    r: colors[0],
    g: colors[1],
    b: colors[2],
  }
}

export const updateColorOptionsOnAnnotator = () => {
  updatePaintObservation();
  const activeColors = [];
  const colorParams = {
    eraser: {r: 1, g: 1, b: 1},
  };
  const tableData = PaintTable.getData("active");
  let targetColorId = null;
  for (const row of tableData) {
    colorParams[row.id] = {r: row.r / 255, g: row.g / 255, b: row.b / 255};
    if(row.target) {
      targetColorId = row.id;
    } else if (row.visibility) {
      activeColors.push(row.id);
    }
  }
  if(targetColorId) {
    activeColors.unshift(targetColorId);
  }

  let colorOptions = {
    activeColors: activeColors,
    colorParams: colorParams,
    eraser: !APP.paint_on,
    overwrite: APP.paint_overwriteB
  }
  setColorOptions(colorOptions, {meshes: APP.getMeshes()});
};

export const PaintTable = new Tabulator('#PaintTable', {
	layout:"fitColumns",
	autoResize:true,
	responsiveLayout:"hide",
	tooltips:true,
	addRowPos:"top",
	history:true,
	pagination:"local",
	paginationSize:10,
	resizableRows:true,
	movableRows: true,
	initialSort:[],
	columns:[
      {title: "Delete", formatter: "buttonCross",  hozAlign: "center", cellClick: (e, cell) => {cell.getRow().delete()}, headerSort:false},
      {title: "Visible", field:"visibility", width: 73, hozAlign:"center", formatter:"tickCross", headerSort:false, cellClick: (e, cell)=>{
        const value = cell.getRow().getData();
        cell.setValue(!value.visibility || value.target);
        updateColorOptionsOnAnnotator();
        updateMetricsOnPaintTable();
    }},
      {title: "Target", field:"target", width: 73, hozAlign:"center", formatter:"tickCross", headerSort:false, cellClick: (e, cell)=>{
        const table = PaintTable;
        const value = cell.getRow().getData();
        table.setData(table.getData("active").map(item => { 
          item = Object.assign({}, item);
          item.debug = true;
          item.target = value.id == item.id;
          item.visibility = item.visibility || item.target;
          return item;  
        }))
        updateColorOptionsOnAnnotator();
      }},
	    {title: "ID", field:"id", width: 40, headerSort:false},
	    {title: "Name", field: "name", editor: "input", headerSort:false, cellEdited: () => updateColor()},
   	  {title: "R", field: "r", minWidth: 30, width: 35, hozAlign: "right", visible: true, editor: "number", editorParams: {min:0, max: 255, step: 1}, mutator: mutatorClip, mutatorParams: mutatorParamsClip, headerSort:false, cellEdited: () => updateColor()},
	    {title: "G", field: "g", minWidth: 30, width: 35, hozAlign: "right", visible: true, editor: "number", editorParams: {min:0, max: 255, step: 1}, mutator: mutatorClip, mutatorParams: mutatorParamsClip, headerSort:false, cellEdited: () => updateColor()},
	    {title: "B", field: "b", minWidth: 30, width: 35, hozAlign: "right", visible: true, editor: "number", editorParams: {min:0, max: 255, step: 1}, mutator: mutatorClip, mutatorParams: mutatorParamsClip, headerSort:false, cellEdited: () => updateColor()},
	    {title: "Area", field: "area", headerSort:false, formatter: "money", formatterParams: {precision: 5}},
	    {title: "Volume", field: "volume", headerSort:false, formatter: "money", formatterParams: {precision: 5}},
	    {title: "Area reserv", field: "area_reserv", headerSort:false, formatter: "money", formatterParams: {precision: 5}, visible: false},
	    {title: "Length", field: "length", headerSort:false, formatter: "money", formatterParams: {precision: 5}, visible: false},
	    {title: "Max r", field: "max_radius", headerSort:false, formatter: "money", formatterParams: {precision: 5}, visible: false},
	    {title: "Mean r", field: "max_radius", headerSort:false, formatter: "money", formatterParams: {precision: 5}, visible: false},
	    {title: "Min r", field: "min_radius", headerSort:false, formatter: "money", formatterParams: {precision: 5}, visible: false}
	],  
  rowMoved: (row) => {
    updateColor();
  },
  rowDeleted: (row) => {
    updateColor();
  },
  rowAdded: (row) => {
    updateColor();
  }
});


const updateColor = () => {
  updateColorOptionsOnAnnotator()
  paintManager.updateList({ list: PaintTable.getData(), lastPaintId })
};

window.switchAnnotation = (checked) => {
	APP.paint_mode = checked;
	APP.controls.noRotate = checked;
}; 

window.switchEraserAnnotation = (checked) => {
	APP.paint_on = checked;
  updateColorOptionsOnAnnotator()
};

window.setAnnotationOverwrite = (checked) => {
  APP.paint_overwriteB = checked;
  updateColorOptionsOnAnnotator()
}

let lastPaintId = 0;
$('#button-add-paint-layer').on('click', (event) => {
    lastPaintId++;
    const hasTarget = PaintTable.getData("active").some(item => item.target);
    var layer = Object.assign({id: lastPaintId, name: "Layer" + String(lastPaintId), area:0, volume: 0, visibility: true, target: !hasTarget}, getRandomColor(lastPaintId));
    PaintTable.addData(layer);
    updateColorOptionsOnAnnotator()
});

$('#save-paint-table-csv').on('click', (event) => {
  downloadPaintTableAsCSV();
});


//// 201016

$('#calc-volumes').on('click', (event) => {
	paintManager.updatePaintVolumes()
});


//// 211223
const downloadPaintTableAsCSV = () => {
  const tableData = PaintTable.getData("active");
  const csvData = [["id", "name", "r", "g", "b", "area", "volume", "area_reserv", "length","max_radius","mean_radius","min_radius"]]
  for (const row of tableData) {
    csvData.push([row.id, row.name, row.r, row.g, row.b, row.area, row.volume, row.area_reserv, row.length, row.max_radius, row.mean_radius, row.min_radius]);
  }

  const csvContent = "data:text/csv;charset=utf-8," +
  csvData.map(e => e.join(",")).join("\n");
  const encodeUri = encodeURI(csvContent);
  // window.open(encodeUri); This also download CSV file
  
  const link = document.createElement("a");
  link.setAttribute("href", encodeUri);
  link.setAttribute("download", "paint.csv");
  document.body.appendChild(link);
  link.click();
};

const syncSequence = true;

paintManager.emitter.on("update", data => {
  if(data.room_id === "list") {
    const currentRows = PaintTable.getData() || [];
    const incomingRows = data.list || [];

    console.log(incomingRows);

    if(syncSequence) { 
      const currentRowsMap = new Map(currentRows.map(currentRow => [currentRow.id, currentRow]));
      PaintTable.setData(incomingRows.map(incomingRow => {
        const currentRow = currentRowsMap.get(incomingRow.id);
        return {
          visibility: true,
          ...currentRow,
          id: incomingRow.id,
          name: incomingRow.name,
          r: incomingRow.r,
          g: incomingRow.g,
          b: incomingRow.b,
          volume: incomingRow.volume,
          area_reserv: incomingRow.area_reserv,
          length: incomingRow.length,
          max_radius: incomingRow.max_radius,
          mean_radius: incomingRow.mean_radius,
          min_radius: incomingRow.min_radius,
        }
      }));
    } else {
      const incomingRowsMap = new Map(incomingRows.map(incomingRow => [incomingRow.id, incomingRow]));
      const newRows = [];
      for(const currentRow of currentRows) {
        if(incomingRowsMap.has(currentRow.id)) {
          const incomingRow = incomingRowsMap.get(currentRow.id);
          newRows.push({
            ...currentRow,
            name: incomingRow.name,
            r: incomingRow.r,
            g: incomingRow.g,
            b: incomingRow.b,
          	volume: incomingRow.volume,
          	area_reserv: incomingRow.area_reserv,
          	length: incomingRow.length,
          	max_radius: incomingRow.max_radius,
          	mean_radius: incomingRow.mean_radius,
          	min_radius: incomingRow.min_radius,
          })
          incomingRowsMap.delete(currentRow.id);
        }
      }
      for(const [id, incomingRow] of incomingRowsMap) {
        newRows.push({
          id: incomingRow.id,
          visibility: true,
          name: incomingRow.name,
          r: incomingRow.r,
          g: incomingRow.g,
          b: incomingRow.b,
          volume: incomingRow.volume,
          area_reserv: incomingRow.area_reserv,
          length: incomingRow.length,
          max_radius: incomingRow.max_radius,
          mean_radius: incomingRow.mean_radius,
          min_radius: incomingRow.min_radius,
        });
      }
      PaintTable.setData(newRows);
    }
    lastPaintId = data.lastPaintId || 0;
    updateColorOptionsOnAnnotator()
  }
})
