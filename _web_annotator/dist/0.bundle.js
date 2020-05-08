(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[0],{

/***/ "./js/APP.js":
/*!*******************!*\
  !*** ./js/APP.js ***!
  \*******************/
/*! exports provided: APP */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "APP", function() { return APP; });
const APP = {};
window.APP = APP;

/***/ }),

/***/ "./js/AnnotationTable.js":
/*!*******************************!*\
  !*** ./js/AnnotationTable.js ***!
  \*******************************/
/*! exports provided: updateColorOptionsOnAnnotator, AnnotationTable */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "updateColorOptionsOnAnnotator", function() { return updateColorOptionsOnAnnotator; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AnnotationTable", function() { return AnnotationTable; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");


const mutatorClip = (value, data, type, mutatorParams, component) => {
  const min = mutatorParams.min;
  const max = mutatorParams.max;
  return value <= min ? min : value >= max ? max : value;
};

const mutatorParamsClip = {
  min: 0,
  max: 255
}; // 0-1までのなるべく離れた値を返す

const reversalBit = index => {
  let original = index,
      fraction = 1,
      value = 0;

  while (original) {
    const bit = original % 2;
    original = (original - bit) / 2;
    fraction /= 2;
    value += bit * fraction;
  }

  return value;
}; // 彩度が最大で、なるべく異なる色相の色を返す


const getRandomColor = index => {
  const value = reversalBit(index - 1) % 1 * 3;
  const mainColorType = Math.floor(value);
  const subColorValue = Math.floor((value - mainColorType) * 255);
  const colors = [subColorValue, 255 - subColorValue];
  colors.splice(mainColorType, 0, 0);
  return {
    r: colors[0],
    g: colors[1],
    b: colors[2]
  };
};

const updateColorOptionsOnAnnotator = () => {
  const activeColors = [];
  const colorParams = {
    eraser: {
      r: 1,
      g: 1,
      b: 1
    }
  };
  const tableData = AnnotationTable.getData("active");
  let targetColorId = null;

  for (const row of tableData) {
    colorParams[row.id] = {
      r: row.r / 255,
      g: row.g / 255,
      b: row.b / 255
    };

    if (row.target) {
      targetColorId = row.id;
    } else if (row.visibility) {
      activeColors.push(row.id);
    }
  }

  if (targetColorId) {
    activeColors.unshift(targetColorId);
  }

  let colorOptions = {
    activeColors: activeColors,
    colorParams: colorParams,
    eraser: !_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_paint_mode,
    overwrite: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_overwrite
  };
  console.log(colorOptions);
  setColorOptions(colorOptions, {
    meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes()
  });
};
const AnnotationTable = new Tabulator('#AnnotationTable', {
  layout: "fitColumns",
  autoResize: true,
  responsiveLayout: "hide",
  tooltips: true,
  addRowPos: "top",
  history: true,
  pagination: "local",
  paginationSize: 10,
  resizableRows: true,
  //selectable: 1,
  movableRows: true,
  initialSort: [{
    column: "id",
    dir: "dsc"
  }],
  columns: [{
    title: "Delete",
    formatter: "buttonCross",
    hozAlign: "center",
    cellClick: (e, cell) => {
      cell.getRow().delete();
    },
    headerSort: false
  }, {
    title: "Visible",
    field: "visibility",
    width: 73,
    hozAlign: "center",
    formatter: "tickCross",
    headerSort: false,
    cellClick: (e, cell) => {
      const value = cell.getRow().getData();
      cell.setValue(!value.visibility || value.target);
      updateColorOptionsOnAnnotator();
    }
  }, {
    title: "Target",
    field: "target",
    width: 73,
    hozAlign: "center",
    formatter: "tickCross",
    headerSort: false,
    cellClick: (e, cell) => {
      const table = AnnotationTable;
      const value = cell.getRow().getData();
      table.setData(table.getData("active").map(item => {
        item = Object.assign({}, item);
        item.debug = true;
        item.target = value.id == item.id;
        item.visibility = item.visibility || item.target;
        return item;
      }));
      updateColorOptionsOnAnnotator();
    }
  }, {
    title: "ID",
    field: "id",
    width: 40
  }, {
    title: "Name",
    field: "name"
  }, {
    title: "R",
    field: "r",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    visible: true,
    editor: "number",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    },
    mutator: mutatorClip,
    mutatorParams: mutatorParamsClip,
    headerSort: false
  }, {
    title: "G",
    field: "g",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    visible: true,
    editor: "number",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    },
    mutator: mutatorClip,
    mutatorParams: mutatorParamsClip,
    headerSort: false
  }, {
    title: "B",
    field: "b",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    visible: true,
    editor: "number",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    },
    mutator: mutatorClip,
    mutatorParams: mutatorParamsClip,
    headerSort: false
  }, {
    title: "Area",
    field: "area"
  }, {
    title: "Volume",
    field: "volume"
  }],
  rowMoved: row => {
    updateColorOptionsOnAnnotator();
  },
  rowDeleted: row => {
    updateColorOptionsOnAnnotator();
  }
});

window.switchAnnotation = checked => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_mode = checked;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.noRotate = checked;
};

window.switchEraserAnnotation = checked => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_paint_mode = checked;
  updateColorOptionsOnAnnotator();
};

window.setAnnotationOverwrite = checked => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_overwrite = checked;
  updateColorOptionsOnAnnotator();
};

let annotationId = 0;
$('#button-add-annotation-layer').on('click', event => {
  annotationId++;
  const hasTarget = AnnotationTable.getData("active").some(item => item.target);
  var layer = Object.assign({
    id: annotationId,
    name: "Layer" + String(annotationId),
    area: 0,
    volume: 0,
    visibility: true,
    target: !hasTarget
  }, getRandomColor(annotationId));
  AnnotationTable.addData(layer);
  updateColorOptionsOnAnnotator();
});
$('#save-annotation-table-csv').on('click', event => {
  downloadAnnotationTableAsCSV();
});

const downloadAnnotationTableAsCSV = () => {
  const tableData = AnnotationTable.getData("active");
  const csvData = [["id", "name", "r", "g", "b", "area"]];

  for (const row of tableData) {
    csvData.push([row.id, row.name, row.r, row.g, row.b]);
  }

  const csvContent = "data:text/csv;charset=utf-8," + csvData.map(e => e.join(",")).join("\n");
  const encodeUri = encodeURI(csvContent); // window.open(encodeUri); This also download CSV file

  const link = document.createElement("a");
  link.setAttribute("href", encodeUri);
  link.setAttribute("download", "annotation.csv");
  document.body.appendChild(link);
  link.click();
};

/***/ }),

/***/ "./js/ControlAnnotator.js":
/*!********************************!*\
  !*** ./js/ControlAnnotator.js ***!
  \********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
 //
// Shared
//

window.ChangeMode = function (mode) {
  switch (mode) {
    case "view":
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      break;

    case "point":
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 1;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      break;

    case "paint":
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = true;
      switchAnnotation(1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      break;

    case "skeleton":
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 1;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletons();
      break;

    default:
      console.log(`Error. Mode ${mode} cannot be interpreted.`);
  }
}; //
// app/index.jsで使っている
//


window.MarkerOffOn = function (ischecked) {
  if (ischecked == true) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerOffOn = 1;
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerOffOn = 0;
  }
};

window.SaveImage = function (ischecked) {
  let canvas = document.getElementById("myCanvas").querySelector('canvas');
  let link = document.createElement("a");
  link.href = canvas.toDataURL("image/png");
  link.download = "Screenshot.png";
  link.click();
}; //
// View
//


window.BackgroundWhiteBlack = function (ischecked) {
  if (ischecked == true) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].setBackGroundColor(0x000000);
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BackGroundColor = 'Black';
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].setBoundingBoxColor(0xffffff);
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].setBackGroundColor(0xffffff);
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BackGroundColor = 'White';
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].setBoundingBoxColor(0x000000);
  }
};

window.FrameOffOn = function (ischecked) {
  if (ischecked == true) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addBoundingBox();
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeBoundingBox();
  }
};

window.DirLight = function (isnum) {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.intensity = isnum / 100;
};

window.AmbLight = function (isnum) {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight.intensity = isnum / 100;
};

window.CenterXY = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.up.set(0, 0, 1);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax * 3.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.target.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
};

window.CenterYZ = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.up.set(0, 1, 0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax * 3.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.target.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
};

window.CenterZX = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.up.set(1, 0, 0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax * 3.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.target.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
}; //
// Skeleton
//
//
// Paint
//
// Eraser, Radius, Overwrite

/***/ }),

/***/ "./js/HandleBasement.js":
/*!******************************!*\
  !*** ./js/HandleBasement.js ***!
  \******************************/
/*! exports provided: launchAnnotator */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "launchAnnotator", function() { return launchAnnotator; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _AnnotationTable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./AnnotationTable */ "./js/AnnotationTable.js");


var xratio = 0.6;
var yratio = 0.95;
var frustumSize = 1000;

function animate() {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.render(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.update();
  requestAnimationFrame(animate);
}

;
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].dragging = false;
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_mode = false;
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_paint_mode = true;
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_overwrite = false; // ObtainWindowSize

function onWindowResize() {
  var aspect = window.innerWidth / window.innerHeight;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.left = -frustumSize * aspect / 2;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.right = frustumSize * aspect / 2;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.top = frustumSize / 2;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.bottom = -frustumSize / 2;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.updateProjectionMatrix();
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.setSize(window.innerWidth * xratio, window.innerHeight * yratio);
} // Draw bounding box


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addBoundingBox = function () {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BackGroundColor == 'Black') {
    var mat = new THREE.LineBasicMaterial({
      color: 0xFFFFFF,
      linewidth: 2
    });
  } else {
    var mat = new THREE.LineBasicMaterial({
      color: 0x000000,
      linewidth: 2
    });
  }

  var geometry = new THREE.BoxBufferGeometry(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX);
  var geo = new THREE.EdgesGeometry(geometry); // or WireframeGeometry( geometry )

  var boundingbox = new THREE.LineSegments(geo, mat);
  boundingbox.name = 'BoundingBox';
  boundingbox.scale.set(1, 1, 1);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(boundingbox);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingBox = 'On';
  boundingbox.translateX(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2);
  boundingbox.translateY(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2);
  boundingbox.translateZ(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2);
};

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeBoundingBox = function () {
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName('BoundingBox');

  if (obj != undefined) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.remove(obj);
  }

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingBox = 'Off';
};

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].setBoundingBoxColor = function (objcolor) {
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName('BoundingBox');

  if (obj != undefined) {
    obj.material.color.setHex(objcolor);
  }
}; // Set background color


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].setBackGroundColor = function (backcolor) {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.background = new THREE.Color(backcolor);
}; // Operation on mouse click


function clickPosition(event) {
  onDragStart(event); // Location of mouse

  var clientX = event.clientX;
  var clientY = event.clientY; // Normalization of location

  var mouse = new THREE.Vector2();
  mouse.x = (clientX - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.offsetLeft) / _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.clientWidth * 2 - 1;
  mouse.y = -((clientY - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.offsetTop) / _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.clientHeight) * 2 + 1; // Raycasterインスタンス作成

  var raycaster = new THREE.Raycaster(); // 取得したX、Y座標でrayの位置を更新

  raycaster.setFromCamera(mouse, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera); // Indetify crossing objects.

  var intersects_org = raycaster.intersectObjects(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.children);
  var intersected_filtered = [];

  for (let i = 0; i < intersects_org.length; i++) {
    var name = intersects_org[i].object.name; // console.log(name)

    if (name !== 'cursor' && name !== 'BoundingBox') {
      intersected_filtered.push(intersects_org[i]);
    }
  } // Put a marker if in the marker mode (this should be moved to HandleMarker.js).
  // Show the ID if not.


  if (intersected_filtered.length > 0) {
    // Get the most proximal one
    var name = intersected_filtered[0].object.name;
    const target = document.getElementById("ClickedObjectID");
    target.innerHTML = name;

    if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode == 1) {
      var x = intersected_filtered[0].point.x;
      var y = intersected_filtered[0].point.y;
      var z = intersected_filtered[0].point.z; //Append Jsontable

      var markerName = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerPrefix + String(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerSuffix);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addMarker({
        act: 1,
        name: markerName,
        parentid: name,
        radius: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerRadius,
        r: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerR,
        g: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerG,
        b: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerB,
        x: x,
        y: y,
        z: z
      });
    }
  } else {
    const target = document.getElementById("ClickedObjectID");
    target.innerHTML = "Background";
  }
}

var onDragStart = event => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].dragging = true;
  annotate(event);
};

var onDragEnd = event => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].dragging = false;
};

var annotate = event => {
  if (!_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].dragging) {
    const {
      intersect
    } = getIntersect({
      x: event.offsetX,
      y: event.offsetY,
      camera: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera,
      meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes(),
      container: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement
    });
    updateCursor(intersect && intersect.point);
    return;
  }

  ;
  if (!_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].annotation_mode) return;
  const {
    intersect
  } = annotateBySphere({
    x: event.offsetX,
    y: event.offsetY,
    camera: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera,
    meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes(),
    container: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement,
    radius: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].AnnotatorRadius || 3,
    ignoreBackFace: null
  });
  updateCursor(intersect && intersect.point);
  updateMetricsOnAnnotationTable(_AnnotationTable__WEBPACK_IMPORTED_MODULE_1__["AnnotationTable"]);
};

const updateCursor = position => {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible === false) {
    return;
  }

  const radius = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].AnnotatorRadius || 3;
  const cursor = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor;

  if (position) {
    cursor.position.copy(position);
    const zoom = radius / cursor.geometry.boundingSphere.radius;
    cursor.scale.set(zoom, zoom, zoom);
    cursor.opacity = 0.3;
  } else {
    cursor.opacity = 0;
  }
};

const updateMetricsOnAnnotationTable = annotationTable => {
  const params = getCurrentParams({
    meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes()
  });
  const areas = params.areas;
  const newRows = annotationTable.getData("active").map(_item => {
    const item = Object.assign({}, _item);
    item.area = areas[item.id] && areas[item.id].toFixed(0);
    return item;
  });
  annotationTable.updateData(newRows);
};

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes = () => {
  return _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.children.filter(object => object.type === "Mesh" && object.geometry.isBufferGeometry && !object.isCursor);
};

function launchAnnotator() {
  // Renderer
  var container = document.getElementById('myCanvas');
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer = new THREE.WebGLRenderer({
    preserveDrawingBuffer: true
  });
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.setSize(window.innerWidth * xratio, window.innerHeight * yratio);
  container.appendChild(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement); // Initilize camera

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera = new THREE.PerspectiveCamera(); // Scene

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene = new THREE.Scene();
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera); // Background Color

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.background = new THREE.Color(0xffffff);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BackGroundColor == 'White'; // Light

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight = new THREE.DirectionalLight(0xffffff);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.set(1, 1, 1);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.intensity = 0.8;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.add(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight = new THREE.AmbientLight(0xffffff);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight.intensity = 0.5;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.add(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight);
  var min = 0;
  var max = 255; // Controlsを用意

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls = new THREE.TrackballControls(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.rotateSpeed = 10;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.staticMoving = false;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.dynamicDampingFactor = 1.0; // staticMoving = false のときの減衰量

  animate(); // Response to mouse click

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.addEventListener('mousedown', clickPosition, false);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.addEventListener('mouseup', onDragEnd, false);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.addEventListener('onmousemove', annotate, false);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.onmousemove = annotate; // Paint
  // Cursor

  var geometry = new THREE.SphereBufferGeometry(3, 32, 32);
  var material = new THREE.MeshLambertMaterial({
    color: 0xffffff,
    opacity: 0.3,
    transparent: true,
    depthWrite: false
  });
  var cursor = new THREE.Mesh(geometry, material);
  cursor.isCursor = true;
  cursor.name = 'cursor';
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor = cursor;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(cursor); // Marker

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerR = 255;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerG = 0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerB = 0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerPrefix = "Marker";
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerSuffix = 0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerRadius = 2.0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerID = 1; // Surface opacity

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = 1.0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity_reserved = 0.5; // Skeleton

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0; //Boundingbox

  const call_url = location.protocol + "//" + location.host + "/surface/Boundingbox.json";
  $.getJSON(call_url).done(function (data) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX = data.x;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY = data.y;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ = data.z;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax = Math.max(data.x, data.y, data.z);
    window.CenterXY();
  });
}
window.addEventListener('resize', onWindowResize, false);

/***/ }),

/***/ "./js/HandleMarkers.js":
/*!*****************************!*\
  !*** ./js/HandleMarkers.js ***!
  \*****************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");
/* harmony import */ var _MarkerTable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./MarkerTable */ "./js/MarkerTable.js");
//
//
//
//
//



/**
 * マーカーを追加する
 *
 * @param {Object} markerData CSVで読み込まれたプロパティを持つオブジェクト。以下のプロパティが有効
 *   - act      : {number} 例: 1
 *   - name     : {string} 例: "Marker1"
 *   - parentid : {number} 例: 3036
 *   - radius   : {number} 例: 2.8
 *   - r        : {number} 例: 255
 *   - g        : {number} 例: 30
 *   - b        : {number} 例: 100
 *   - x        : {number} 例: 9.076891761740626
 *   - y        : {number} 例: 10.850928915374125
 *   - z        : {number} 例: 252.16774396931498
 *
 * @param {bool} [isImportFromFile=false] ファイルからの読み込みかどうか。
 *   ファイルからの読み込み時はMarkerがOFFでもMarkerTableに追加する
 * @return {bool} マーカーを追加したらtrueが返る
 */

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addMarker = function (markerData, isImportFromFile) {
  var markerData_act = Number(markerData.act);
  var markerData_name = String(markerData.name);
  var markerData_parentid = Number(markerData.parentid);
  var markerData_radius = Number(markerData.radius);
  var markerData_r = Number(markerData.r);
  var markerData_g = Number(markerData.g);
  var markerData_b = Number(markerData.b);
  var markerData_x = Number(markerData.x);
  var markerData_y = Number(markerData.y);
  var markerData_z = Number(markerData.z); // CSVファイルからの読み込み時はMarkerがOFFでも描画する(要確認)

  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode == 1 || isImportFromFile) {
    var color = rgb2hex([markerData_r, markerData_g, markerData_b]); // Add sphere

    var geometry = new THREE.SphereGeometry(1);
    var material = new THREE.MeshBasicMaterial({
      color: color
    });
    var sphere = new THREE.Mesh(geometry, material);
    sphere.scale.set(markerData_radius, markerData_radius, markerData_radius);
    sphere.position.set(markerData_x, markerData_y, markerData_z);
    sphere.name = 'm' + _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerID.toString();
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(sphere);
    var NewMarker = {
      act: markerData_act,
      id: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerID,
      name: markerData_name,
      parentid: markerData_parentid,
      radius: markerData_radius,
      r: markerData_r,
      g: markerData_g,
      b: markerData_b,
      x: markerData_x,
      y: markerData_y,
      z: markerData_z
    };
    _MarkerTable__WEBPACK_IMPORTED_MODULE_2__["MarkerTable"].addData(NewMarker); // Change database MarkerTable (setData)

    updateMarkerId();
    return true;
  }

  return false;
};

function rgb2hex(rgb) {
  return "#" + rgb.map(function (value) {
    return ("0" + value.toString(16)).slice(-2);
  }).join("");
}
/**
 * MarkerIDを更新する
 */


function updateMarkerId() {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerSuffix = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerSuffix + 1;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerID = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerID + 1;
  $('#SetSuffixNum').val(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerSuffix); // Change suffix for index.html
}

;
/**
 * マーカーを描画する
 *
 * @example
 * renderMarker({
 *   "act": 1,
 *   "name": "test1",
 *   "parentid": 3000,
 *   "radius": 2,
 *   "r": 100,
 *   "g": 0,
 *   "b": 0,
 *   "x": 100,
 *   "y": 200,
 *   "z": 200
 * })
 *
 * @param {Object} markerData CSVで読み込まれたプロパティを持つオブジェクト。addMarkerの引数と同じ
 */

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderMarker = function (markerData) {
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(Number(markerData.parentid));

  if (obj == null) {
    return false;
  }

  return _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addMarker(markerData, true);
}; // Change the color of the stl object specified by a name after generation.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeMarkerRadius = function (id, r) {
  var name = 'm' + id.toString();
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);
  console.log(obj);

  if (obj != undefined) {
    obj.scale.set(r, r, r);
  }
}; // Change the color of the stl object specified by a name after generation.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeMarkerColor = function (id, objcolor) {
  var name = 'm' + id.toString();
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    obj.material.color.setHex(objcolor);
  }
}; // Remove a stl object by a name after generation.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeMarker = function (id) {
  // Remove from scene
  var name = 'm' + id.toString();
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.remove(obj);
  }
};

/***/ }),

/***/ "./js/HandleSkeletons.js":
/*!*******************************!*\
  !*** ./js/HandleSkeletons.js ***!
  \*******************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");
//
//
//
//
//

 // Change the opacity of all surface objects

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletons = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.traverse(function (obj) {
    if (obj instanceof THREE.Mesh === true && obj.name.length === 10) {
      var id = obj.name - 0;
      var col = obj.material.color;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject(id, col);
    }
  });
};

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.traverse(function (obj) {
    if (obj.name.match(/line/)) {
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.remove(obj);
    }
  });
}; // Add stl objects and a name


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject = function (id, col) {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode == 0) {
    return false;
  }

  const target_url = location.protocol + "//" + location.host + "/skeleton/whole/" + ('0000000000' + id).slice(-10) + ".hdf5";
  const filename = ('0000000000' + id).slice(-10) + ".hdf5";
  fetch(target_url).then(function (response) {
    return response.arrayBuffer();
  }).then(function (buffer) {
    //
    //
    var f = new hdf5.File(buffer, filename);
    let g1 = f.get('vertices');
    let g2 = f.get('edges');
    var data_vertices = g1.value;
    var data_edges = g2.value;
    data_vertices = splitArray(data_vertices, 3);
    data_edges = splitArray(data_edges, 2);
    var i1 = undefined;
    var i2 = undefined;
    var v1 = undefined;
    var v2 = undefined; // console.log(data_vertices)
    // console.log('Length vertices: ' + data_vertices.length);
    // console.log('Length edges   : ' + data_edges.length);

    if (isNaN(data_vertices[0][0]) == true) {
      // console.log(data_vertices);
      console.log('No morphological data.');
      return false;
    }

    var geometry = new THREE.Geometry();
    var material = new THREE.LineBasicMaterial({
      color: col,
      //0x000000
      linewidth: 3,
      fog: true
    });
    var scale_factor_xy = 5;
    var xscale = 1.0 / Math.pow(2, scale_factor_xy);
    var yscale = 1.0 / Math.pow(2, scale_factor_xy);
    var zscale = 1.0 / 40;

    for (var i = 0; i < data_edges.length; i++) {
      i1 = data_edges[i][0];
      i2 = data_edges[i][1]; // console.log('Vertices ID: ', i1, i2 );

      v1 = new THREE.Vector3(data_vertices[i1][0] * zscale, data_vertices[i1][2] * yscale, data_vertices[i1][1] * xscale);
      v2 = new THREE.Vector3(data_vertices[i2][0] * zscale, data_vertices[i2][2] * yscale, data_vertices[i2][1] * xscale);
      geometry.vertices.push(v1, v2);
    }

    var line = new THREE.LineSegments(geometry, material);
    line.name = 'line' + ('0000000000' + id).slice(-10); // console.log(line.name);

    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(line); //
    //
    //
  });
}; // Change the color of a skeleton object specified by a name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSkeletonObjectColor = function (id, col) {
  name = 'line' + ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name_centerline);

  if (obj != undefined) {
    obj.material.color.setHex(col);
  }
}; // Remove a stl object by the name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletonObject = function (id) {
  name = 'line' + ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.remove(obj);
  }
};

function splitArray(array, part) {
  var tmp = [];

  for (var i = 0; i < array.length; i += part) {
    tmp.push(array.slice(i, i + part));
  }

  return tmp;
}

/***/ }),

/***/ "./js/HandleSurfaces.js":
/*!******************************!*\
  !*** ./js/HandleSurfaces.js ***!
  \******************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");
/* harmony import */ var _AnnotationTable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./AnnotationTable */ "./js/AnnotationTable.js");
//
//
//
//
//


 // Add surface objects and a name

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSurfaceObject = function (id, col) {
  const name = ('0000000000' + id).slice(-10);
  const call_url = location.protocol + "//" + location.host + "/ws/surface?id=";
  const target_url = location.protocol + "//" + location.host + "/surface/whole/" + name + ".stl"; // Revive it if already exists.
  // console.log('Name: ', name)

  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // console.log('Obj: ', obj)
    obj.visible = true;
    return true;
  } // Request the surface mesh generation to the server if it does not exist.


  var xhr = new XMLHttpRequest();
  xhr.open("HEAD", target_url, false); //同期モード

  xhr.send(null);

  if (xhr.status == 404) {
    var req = new XMLHttpRequest();
    req.open("get", call_url + id, false);
    req.send(null);

    if (req.responseText == "False") {
      alert("No surface.");
      return false;
    }
  } // console.log('Mesh prepared.');
  // Load the stl file then generate mesh object.


  var loader = new THREE.STLLoader();
  loader.load(target_url, function (bufferGeometry) {
    if (bufferGeometry.isBufferGeometry) {
      bufferGeometry.attributes.color = bufferGeometry.attributes.color || bufferGeometry.attributes.position.clone();
      bufferGeometry.attributes.color.array.fill(1);
      bufferGeometry.attributes.color.needsUpdate = true;
      bufferGeometry.colorsNeedUpdate = true;
    } // console.log('Stl loaded.');


    const meshMaterial = new THREE.MeshPhongMaterial({
      color: col,
      specular: 0x776666,
      shininess: 0.2,
      vertexColors: THREE.FaceColors,
      transparent: true,
      opacity: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity,
      side: true
    }); // APP.surface_opacity

    var mesh = new THREE.Mesh(bufferGeometry, meshMaterial);
    mesh.name = name;
    mesh.scale.set(1, 1, 1);
    mesh.material.side = THREE.DoubleSide;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(mesh); // console.log(mesh.name);

    Object(_AnnotationTable__WEBPACK_IMPORTED_MODULE_2__["updateColorOptionsOnAnnotator"])();
  });
}; // Change the opacity of all surface objects


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity = function (opacity) {
  // console.log('Input opacity: ', opacity)
  if (opacity == -1) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = 1;
  } else if (opacity == 0) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity_reserved;
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = opacity;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity_reserved = opacity;
  }

  ;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.traverse(function (obj) {
    if (obj instanceof THREE.Mesh === true && obj.name !== 'cursor') {
      obj.material.opacity = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity;
    } // console.log('Obj name:', obj.name );

  });
}; // Change the color of a surface object specified by the name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectColor = function (id, objcolor) {
  name = ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    obj.material.color.setHex(objcolor);
  }
}; // Remove a stl object by a name after generation.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSurfaceObject = function (id) {
  name = ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // APP.scene.remove(obj);
    obj.visible = false;
  }
};

/***/ }),

/***/ "./js/MarkerTable.js":
/*!***************************!*\
  !*** ./js/MarkerTable.js ***!
  \***************************/
/*! exports provided: MarkerTable */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MarkerTable", function() { return MarkerTable; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");


const MarkerTable = new Tabulator("#MarkerTable", {
  layout: "fitColumns",
  //fit columns to width of table
  autoResize: true,
  responsiveLayout: "hide",
  //hide columns that dont fit on the table
  tooltips: true,
  //show tool tips on cells
  addRowPos: "top",
  //when adding a new row, add it to the top of the table
  history: true,
  //allow undo and redo actions on the table
  pagination: "local",
  //paginate the data
  paginationSize: 10,
  //allow 7 rows per page of data
  resizableRows: true,
  //allow row order to be changed
  initialSort: [//set the initial sort order of the data
  {
    column: "id",
    dir: "dsc"
  }],
  columns: [//define the table columns
  // ActやX,Y,Zはダウンロード時に除外されないよう定義しておく。ただしカラムvisible: falseにして非表示にする
  {
    title: "Act",
    field: "act",
    download: true,
    visible: false
  }, {
    title: "Delete",
    formatter: "buttonCross",
    width: 73,
    hozAlign: "center",
    editor: "tickCross",
    editable: onDeleteCheck,
    download: false
  }, {
    title: "ID",
    field: "id",
    width: 40
  }, // マーカー名を入力する時に日本語などASCII外が入力されないようにする
  // 入力されるとCSVファイルダウンロード→インポートを通して文字化けが発生するため、[ a-zA-Z0-9_-] のみ使用可能とする
  {
    title: "Name",
    field: "name",
    width: 70,
    editor: "input",
    validator: function (cell, value, parameters) {
      return util.isMarkerName(value);
    }
  }, {
    title: "Parent ID",
    field: "parentid",
    width: 70
  }, {
    title: "Radius",
    field: "radius",
    width: 60,
    hozAlign: "right",
    editor: "number",
    editorParams: {
      min: 0.2,
      max: 24,
      step: 0.2
    }
  }, {
    title: "R",
    field: "r",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    editor: "range",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    }
  }, {
    title: "G",
    field: "g",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    editor: "range",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    }
  }, {
    title: "B",
    field: "b",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    editor: "range",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    }
  }, {
    title: "X",
    field: "x",
    download: true,
    visible: false
  }, {
    title: "Y",
    field: "y",
    download: true,
    visible: false
  }, {
    title: "Z",
    field: "z",
    download: true,
    visible: false
  }],
  // セルが編集されたとき
  cellEdited: function (cell) {
    // 渡ってくるパラメータcellについて: http://tabulator.info/docs/4.1/components#component-cell
    // 編集後の値
    var cellValue = cell.getValue(); // 編集前の値

    var cellOldValue = cell.getOldValue(); // 編集対象のセルがある列

    var row = cell.getRow();
    var act = row.getData().act;
    var id = row.getData().id;
    var radius = row.getData().radius;
    var r = row.getData().r;
    var g = row.getData().g;
    var b = row.getData().b;
    var columnField = cell.getColumn().getField();

    if (columnField == 'radius') {
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeMarkerRadius(id, radius);
    }

    if (columnField == 'r' || columnField == 'g' || columnField == 'b') {
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeMarkerColor(id, r * 256 * 256 + g * 256 + b * 1);
    }
  }
}); // 「Import CSV」ボタンを押したとき

$('#import-csv-marker-table').on('change', onImportCSVFileSelect); // 「Clear」ボタンを押したら3Dマーカーをクリアする

$('#clear-marker-table').on('click', function (event) {
  clearMarkerTable();
  return false;
}); // 「Download CSV」ボタンを押したとき

$('#save-marker-table-csv').on('click', function (event) {
  downloadMarkerTableAsCSV();
  return false;
}); // Deleteのチェックが押されたとき

function onDeleteCheck(cell) {
  var data = cell.getRow().getData();
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeMarker(data.id);
  cell.getRow().delete();
} // 「Import CSV」ボタンが押されてファイルを選択したとき


function onImportCSVFileSelect(event) {
  var file = event.originalEvent.target.files[0];
  var reader = new FileReader();

  reader.onload = function (e) {
    var csvFileContent = e.target.result;
    var parsedData = Object(_csv__WEBPACK_IMPORTED_MODULE_1__["parseCSV"])(csvFileContent); // 1行目のタイトルを除外

    parsedData.shift(); // タイトルフィールドを変換

    var markers = replaceColumnTitle(ObjMarkerTable, parsedData); // 同じ座標のためスキップした数

    var sameCoordinatesCount = 0; // Parent ID のオブジェクトが非表示のためスキップした数

    var parentNotVisibleCount = 0;
    markers.forEach(function (markerData) {
      if (!validateMarkerDataType(markerData)) {
        // 不正な値があったらスキップ
        console.error("Invalid marker data", markerData);
      } else if (!validateMarkerDataXYZ(markerData)) {
        // すでに同じ座標で定義済みだったらスキップ
        console.warn("Skipped: The loaded marker has been defined as same coordinates.", markerData);
        sameCoordinatesCount++;
      } else {
        var isAdded = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderMarker(markerData);

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
    } // 選択したファイル情報をクリア。これをしないと同じファイルを再度読み込めない


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
  return ObjMarkerTable.getDataCount() === 0;
}
/**
 * MarkerTableをクリアする
 */


function clearMarkerTable() {
  var rows = ObjMarkerTable.getRows();
  rows.forEach(function (row) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeMarker(row.getData().id);
    row.delete();
  });
}
/**
 * MarkerTableをCSVでダウンロードする
 */


function downloadMarkerTableAsCSV() {
  MarkerTable.download(_csv__WEBPACK_IMPORTED_MODULE_1__["csvFormatter"], 'MarkerTable.csv');
}
/**
 * テーブルカラムのタイトルとフィールドのペアを取得する
 *
 * @example
 * getColumnFieldTitlePairs(ObjMarkerTable)
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
  columnDefinitions.forEach(function (column) {
    fieldTitlePairs[column.title] = column.field;
  });
  return fieldTitlePairs;
}
/**
 * キーがのタイトルのJSONデータをフィールド名にを変換する
 * CSVの1行目タイトルは表記用のものでスペースも含まれるため、内部キー名に変換する
 *
 * @example
 * replaceColumnTitle(ObjMarkerTable, {
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
  return json.reduce(function (memo, data) {
    var newData = {};
    Object.keys(data).forEach(function (key) {
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
  var rows = ObjMarkerTable.getRows();
  return rows.every(function (row) {
    var rowData = row.getData();
    var rowX = rowData.x;
    var rowY = rowData.y;
    var rowZ = rowData.z;
    var markerDataX = Number(markerData.x);
    var markerDataY = Number(markerData.y);
    var markerDataZ = Number(markerData.z); // 浮動小数点数のため、小数点2桁までで比較する。だいたい同じ座標かどうかチェックする

    if (rowX.toFixed(2) === markerDataX.toFixed(2) && rowY.toFixed(2) === markerDataY.toFixed(2) && rowZ.toFixed(2) === markerDataZ.toFixed(2)) {
      // 同じ座標
      return false;
    }

    return true;
  });
}

/***/ }),

/***/ "./js/SurfaceTable.js":
/*!****************************!*\
  !*** ./js/SurfaceTable.js ***!
  \****************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");


var SurfaceTable = new Tabulator("#SurfaceTable", {
  ajaxURL: "./surface/segmentInfo.json",
  layout: "fitColumns",
  //fit columns to width of table
  autoResize: true,
  responsiveLayout: "hide",
  //hide columns that dont fit on the table
  tooltips: true,
  //show tool tips on cells
  addRowPos: "top",
  //when adding a new row, add it to the top of the table
  history: true,
  //allow undo and redo actions on the table
  pagination: "local",
  //paginate the data
  paginationSize: 10,
  //allow 7 rows per page of data
  resizableRows: true,
  //allow row order to be changed
  initialSort: [//set the initial sort order of the data
  {
    column: "name",
    dir: "asc"
  }],
  columns: [//define the table columns
  // ActやConfidenceはダウンロード時に除外されないよう定義しておく。ただしカラムvisible: falseにして非表示にする
  {
    title: "Act",
    field: "act",
    download: true,
    visible: false
  }, {
    title: "Visible",
    field: "act",
    width: 73,
    hozAlign: "center",
    formatter: "tickCross",
    cellClick: (e, cell) => {
      cell.setValue(!cell.getValue());
    },
    download: false
  }, {
    title: "ID",
    field: "id",
    width: 50
  }, {
    title: "Name",
    field: "name",
    editor: "input"
  }, {
    title: "Size",
    field: "size",
    width: 60,
    hozAlign: "right"
  }, {
    title: "Confidence",
    field: "confidence",
    download: true,
    visible: false
  }, {
    title: "R",
    field: "r",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    editor: "range",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    }
  }, {
    title: "G",
    field: "g",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    editor: "range",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    }
  }, {
    title: "B",
    field: "b",
    minWidth: 30,
    width: 35,
    hozAlign: "right",
    editor: "range",
    editorParams: {
      min: 0,
      max: 255,
      step: 1
    }
  }],
  // セルが編集されたとき
  cellEdited: function (cell) {
    // 渡ってくるパラメータcellについて: http://tabulator.info/docs/4.1/components#component-cell
    // 編集後の値
    var cellValue = cell.getValue(); // 編集前の値

    var cellOldValue = cell.getOldValue(); // 編集対象のセルがある列

    var row = cell.getRow();
    var act = row.getData().act;
    var id = row.getData().id;
    var r = row.getData().r;
    var g = row.getData().g;
    var b = row.getData().b; // 編集したセルに対するカラムのフィールド

    var columnField = cell.getColumn().getField(); // console.log("編集後の値:", cellValue, "編集前の値:", cellOldValue, "編集した列:", row, "編集したカラム", columnField);

    var col = r * 256 * 256 + g * 256 + b * 1;

    if (columnField == 'act') {
      if (act == true) {
        console.log("Requested ID:", id);
        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSurfaceObject(id, col);
        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject(id, col);
      }

      if (act == false) {
        console.log("Disappear ID:", id); //const filename = sprintf("./stls/i%d.stl", id );

        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSurfaceObject(id);
        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletonObject(id);
      }
    }

    if (columnField == 'r' || columnField == 'g' || columnField == 'b') {
      console.log("Changecolor ID:", id);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectColor(id, col);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSkeletonObjectColor(id, col);
    }
  }
}); // 「Download CSV」ボタンを押したとき

$('#save-object-table-csv').on('click', function (event) {
  downloadSurfaceTableAsCSV();
  return false;
});
/**
 * ObjectTableをCSVでダウンロードする
 */

function downloadSurfaceTableAsCSV() {
  console.log("downloadObjectTableAsCSV");
  SurfaceTable.download(_csv__WEBPACK_IMPORTED_MODULE_1__["csvFormatter"], 'SurfaceTable.csv');
}

/***/ }),

/***/ "./js/csv.js":
/*!*******************!*\
  !*** ./js/csv.js ***!
  \*******************/
/*! exports provided: csvFormatter, parseCSV */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "csvFormatter", function() { return csvFormatter; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "parseCSV", function() { return parseCSV; });
// TabulatorのcsvFormatterに不具合があるため再定義する
// csvFormatter from Download.prototype.downloaders in tabulator.js
const csvFormatter = function (columns, data, options, setFileContents, config) {
  // TabulatorのcsvFormatterは隠れてるカラムがダウンロード対象にならないためカラムを再定義する
  var columnDefinitions = this.table.getColumnDefinitions();
  columns = columnDefinitions.filter(function (column) {
    return column.download !== false;
  });
  var self = this,
      titles = [],
      fields = [],
      delimiter = options && options.delimiter ? options.delimiter : ",",
      fileContents; //build column headers

  function parseSimpleTitles() {
    columns.forEach(function (column) {
      titles.push('"' + String(column.title).split('"').join('""') + '"');
      fields.push(column.field);
    });
  }

  function parseColumnGroup(column, level) {
    if (column.subGroups) {
      column.subGroups.forEach(function (subGroup) {
        parseColumnGroup(subGroup, level + 1);
      });
    } else {
      titles.push('"' + String(column.title).split('"').join('""') + '"');
      fields.push(column.definition.field);
    }
  }

  if (config.columnGroups) {
    console.warn("Download Warning - CSV downloader cannot process column groups");
    columns.forEach(function (column) {
      parseColumnGroup(column, 0);
    });
  } else {
    parseSimpleTitles();
  } //generate header row


  fileContents = [titles.join(delimiter)];

  function parseRows({
    data
  }) {
    //generate each row of the table
    data.forEach(function (row) {
      var rowData = [];
      fields.forEach(function (field) {
        // getFieldValueを使うと数値がfalseになるため単純にrowの値を使う
        //var value = self.getFieldValue(field, row);
        var value = row[field];

        switch (typeof value) {
          case "object":
            value = JSON.stringify(value);
            break;

          case "undefined":
          case "null":
            value = "";
            break;
        } //escape quotation marks


        rowData.push('"' + String(value).split('"').join('""') + '"');
      });
      fileContents.push(rowData.join(delimiter));
    });
  }

  function parseGroup(group) {
    if (group.subGroups) {
      group.subGroups.forEach(function (subGroup) {
        parseGroup(subGroup);
      });
    } else {
      parseRows(group.rows);
    }
  }

  if (config.rowGroups) {
    console.warn("Download Warning - CSV downloader cannot process row groups");
    data.forEach(function (group) {
      parseGroup(group);
    });
  } else {
    parseRows(data);
  }

  setFileContents(fileContents.join("\n"), "text/csv");
};
/**
 * カンマ区切りのCSV文字列から配列に変換する
 *
 * @param  {string} csv カンマ区切りの文字列
 * @return {Array}  変換した配列
 */

function parseCSV(csv) {
  var result = [];
  var array = csv2array(csv);

  for (var i = 1; i < array.length; i++) {
    result[i - 1] = {};

    for (var k = 0; k < array[0].length && k < array[i].length; k++) {
      var key = array[0][k];
      result[i - 1][key] = array[i][k];
    }
  }

  return result;
}
/**
 * カンマ区切りCSVの一行を配列に変換する
 *
 * 参考: RFC4180 - Common Format and MIME Type for Comma-Separated Values (CSV) Files
 * https://tools.ietf.org/html/rfc4180
 * https://stackoverflow.com/questions/33155999/converting-a-csv-file-into-a-2d-array/33156233
 *
 * @param  {string} csv カンマ区切りの文字列
 * @param  {string} [delimiter=','] 区切り文字。デフォルト=','
 * @return {array} カンマ区切りをを変換した配列
 */

function csv2array(csv, delimiter) {
  delimiter = delimiter || ',';
  var pattern = new RegExp( // [1] delimiter
  '(\\' + delimiter + '|\\r?\\n|\\r|^)' + '(?:' + // [2] quoted value
  '"([^"]*(?:""[^"]*)*)"|' + // [3] standard value
  '([^"\\' + delimiter + '\\r\\n]*)' + ')', 'gi');
  var array = [[]];
  var m, matchedDelimiter, matchedValue;

  while (m = pattern.exec(csv)) {
    matchedDelimiter = m[1];

    if (matchedDelimiter.length && matchedDelimiter !== delimiter) {
      array.push([]);
    }

    if (m[2]) {
      matchedValue = m[2].replace(/""/g, '"');
    } else {
      matchedValue = m[3];
    }

    array[array.length - 1].push(matchedValue);
  }

  return array;
}

/***/ }),

/***/ "./js/init.js":
/*!********************!*\
  !*** ./js/init.js ***!
  \********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _js_ControlAnnotator__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../js/ControlAnnotator */ "./js/ControlAnnotator.js");
/* harmony import */ var _js_csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../js/csv */ "./js/csv.js");
/* harmony import */ var _js_MarkerTable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../js/MarkerTable */ "./js/MarkerTable.js");
/* harmony import */ var _js_util__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../js/util */ "./js/util.js");
/* harmony import */ var _js_util__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_js_util__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _js_SurfaceTable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../js/SurfaceTable */ "./js/SurfaceTable.js");
/* harmony import */ var _js_HandleSurfaces__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../js/HandleSurfaces */ "./js/HandleSurfaces.js");
/* harmony import */ var _js_HandleSkeletons__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../js/HandleSkeletons */ "./js/HandleSkeletons.js");
/* harmony import */ var _js_HandleMarkers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../js/HandleMarkers */ "./js/HandleMarkers.js");
/* harmony import */ var _js_HandleBasement__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../js/HandleBasement */ "./js/HandleBasement.js");









Object(_js_HandleBasement__WEBPACK_IMPORTED_MODULE_8__["launchAnnotator"])();

/***/ }),

/***/ "./js/util.js":
/*!********************!*\
  !*** ./js/util.js ***!
  \********************/
/*! no static exports found */
/***/ (function(module, exports) {

var util = {};
/**
 * 有効な数値かどうかチェックする。文字列なら数値として有効かチェックする
 *
 * @example
 * isNumeric(1) // true
 * isNumeric(123.456) // true
 * isNumeric(0) // true
 * isNumeric(-123) // true
 * isNumeric("abc") // false
 * isNumeric("123") // true
 * isNumeric("-123") // true
 *
 * @param  {string|number} n チェックする対象の値
 * @return {boolean}
 */

util.isNumeric = function (n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};
/**
 * マーカー名として有効かチェック
 * 英数字 [a-zA-Z0-9_-] またはスペースで構成される文字列かどうかチェックする
 *
 * @example
 * isMarkerName('abc') // true
 * isMarkerName('Marker Test 3') // true
 * isMarkerName('マーカー') // false
 *
 * @param  {string} str チェックする対象の文字列
 * @return {boolean}
 */


util.isMarkerName = function (string) {
  return /^(?:[a-zA-Z0-9_-]| )+$/.test(string);
};

/***/ })

}]);
//# sourceMappingURL=0.bundle.js.map