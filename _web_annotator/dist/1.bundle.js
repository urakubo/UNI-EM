(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[1],{

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
// Executed when the window size is changed.

window.addEventListener('resize', function () {
  // サイズを取得
  const width = window.innerWidth;
  const height = window.innerHeight; // カメラのアスペクト比を正す

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.aspect = width * xratio / (height * yratio);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.updateProjectionMatrix(); // レンダラーのサイズを調整する

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.setPixelRatio(window.devicePixelRatio);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.setSize(width * xratio, height * yratio);
}, false); // Mode

window.ChangeMode = function (mode) {
  switch (mode) {
    case "view":
      //			console.log("view")
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSpheres();
      break;

    case "point":
      //			console.log("point")
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 1;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSpheres();
      break;

    case "paint":
      //			console.log("paint")
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = true;
      switchAnnotation(1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-1);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSpheres();
      break;

    case "skeleton":
      //			console.log("skeleton")
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 1;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletons();
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSpheres();
      break;

    case "sphere":
      //			console.log("shpere")
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode = 1;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible = false;
      switchAnnotation(0);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity(-2);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons();
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSpheres();
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
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.background = new THREE.Color(0x000000);
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BackGroundColor = 'Black';
    setBoundingBoxColor(0xffffff);
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.background = new THREE.Color(0xffffff);
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BackGroundColor = 'White';
    setBoundingBoxColor(0x000000);
  }
};

window.DirLight = function (isnum) {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.intensity = isnum / 100;
};

window.AmbLight = function (isnum) {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight.intensity = isnum / 100;
};

window.CenterXY = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.up.set(0, 1, 0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax * 3.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.lookAt(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.target.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0); // APP.renderer.render(APP.scene, APP.camera);
};

window.CenterYZ = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.up.set(0, 0, 1);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax * 3.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.lookAt(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.target.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0); // APP.renderer.render(APP.scene, APP.camera);
};

window.CenterZX = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.up.set(1, 0, 0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax * 3.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.lookAt(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.target.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0); // APP.renderer.render(APP.scene, APP.camera);
};

window.DirLightX = function (ischecked) {
  if (ischecked == true) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.x = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0 + _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax;
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.x = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0 - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax;
  } // APP.renderer.render(APP.scene, APP.camera);

};

window.DirLightY = function (ischecked) {
  if (ischecked == true) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.y = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0 + _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax;
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.y = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0 - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax;
  }
};

window.DirLightZ = function (ischecked) {
  if (ischecked == true) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.z = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0 + _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax;
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.z = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0 - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax;
  }
};

window.FrameOffOn = function (ischecked) {
  if (ischecked == true) {
    addBoundingBox();
  } else {
    removeBoundingBox();
  }
}; // Draw bounding box


function addBoundingBox() {
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

  var geometry = new THREE.BoxBufferGeometry(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ);
  var geo = new THREE.EdgesGeometry(geometry); // or WireframeGeometry( geometry )

  var boundingbox = new THREE.LineSegments(geo, mat);
  boundingbox.name = 'BoundingBox';
  boundingbox.scale.set(1, 1, 1);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(boundingbox);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingBox = 'On';
  boundingbox.translateX(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0);
  boundingbox.translateY(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0);
  boundingbox.translateZ(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0);
}

function removeBoundingBox() {
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName('BoundingBox');

  if (obj != undefined) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.remove(obj);
  }

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingBox = 'Off';
}

function setBoundingBoxColor(objcolor) {
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName('BoundingBox');

  if (obj != undefined) {
    obj.material.color.setHex(objcolor);
  }
}

/***/ }),

/***/ "./js/HandleBasement.js":
/*!******************************!*\
  !*** ./js/HandleBasement.js ***!
  \******************************/
/*! exports provided: updateMetricsOnPaintTable, launchAnnotator */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function(Buffer) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "updateMetricsOnPaintTable", function() { return updateMetricsOnPaintTable; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "launchAnnotator", function() { return launchAnnotator; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _PaintTable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./PaintTable */ "./js/PaintTable.js");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! lodash */ "./node_modules/lodash/lodash.js");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _SyncPaint__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./SyncPaint */ "./js/SyncPaint.js");
/* harmony import */ var _SurfaceTable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./SurfaceTable */ "./js/SurfaceTable.js");
/* harmony import */ var _HandleSurfaces__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./HandleSurfaces */ "./js/HandleSurfaces.js");
/* harmony import */ var zlib__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! zlib */ "./node_modules/browserify-zlib/lib/index.js");
/* harmony import */ var zlib__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(zlib__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _three_annotator_index__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./three_annotator/index */ "./js/three_annotator/index.js");








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
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_mode = false;
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_on = true;
_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_overwriteB = false; // Operation on mouse click

function clickPosition(event) {
  onDragStart(event); // Location of mouse

  var clientX = event.clientX;
  var clientY = event.clientY; // Normalization of location

  var mouse = new THREE.Vector2();
  mouse.x = (clientX - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.offsetLeft) / _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.clientWidth * 2 - 1;
  mouse.y = -((clientY - _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.offsetTop) / _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement.clientHeight) * 2 + 1; // Raycasterインスタンス作成

  var raycaster = new THREE.Raycaster(); // 取得したX、Y座標でrayの位置を更新

  raycaster.setFromCamera(mouse, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera); // Indetify crossing objects.

  var intersects = raycaster.intersectObjects(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.children); // Obtain crossing surface objects.

  var ids = [];
  var intersected_surfaces = [];
  var intersected_objects = [];

  for (let i = 0; i < intersects.length; i++) {
    var name = intersects[i].object.name;

    if (/^\d*$/.test(name) && name.length === 10) {
      // /^\d*$/ 符号や小数点を許容しない数値
      intersected_surfaces.push(intersects[i]); ////

      ids = Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_7__["getPaintID"])({
        x: event.offsetX,
        y: event.offsetY,
        camera: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera,
        meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes(),
        container: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement
      }); ////
      //console.log('ids: ', ids);
    }

    intersected_objects.push(intersects[i]);
  }

  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerMode == 1 && intersected_surfaces.length > 0) {
    // If in the marker mode, put a marker  (this should be moved to HandleMarker.js).
    var x = intersected_surfaces[0].point.x;
    var y = intersected_surfaces[0].point.y;
    var z = intersected_surfaces[0].point.z; //Append Jsontable

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

  const target = document.getElementById("ClickedObjectID");

  if (intersected_objects.length <= 0) {
    target.innerHTML = "Background";
  } else if (typeof ids[0] === "undefined") {
    target.innerHTML = intersected_objects[0].object.name;
  } else {
    target.innerHTML = intersected_objects[0].object.name + "-" + ids[0];
  } // endif

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
    } = Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_7__["getIntersect"])({
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
  if (!_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_mode) return;
  const {
    intersect
  } = Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_7__["annotateBySphere"])({
    x: event.offsetX,
    y: event.offsetY,
    camera: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera,
    meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes(),
    container: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].renderer.domElement,
    radius: getCursorRadius(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].AnnotatorRadius),
    ignoreBackFace: null
  });
  updateCursor(intersect && intersect.point);
  updateMetricsOnPaintTable();
  syncAnnotation();
};

const compress = paintData => paintData && zlib__WEBPACK_IMPORTED_MODULE_6__["gzipSync"](Buffer.from(paintData)).buffer;

const decompress = compressedData => compressedData && new Uint8Array(zlib__WEBPACK_IMPORTED_MODULE_6__["gunzipSync"](Buffer.from(compressedData)).buffer);

const syncAnnotation = lodash__WEBPACK_IMPORTED_MODULE_2___default.a.debounce(() => {
  const changes = Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_7__["getChanges"])({
    meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes()
  });

  if (Object.keys(changes).length > 0) {
    for (const objectChanges of Object.values(changes)) {
      for (const colorChanges of Object.values(objectChanges)) {
        colorChanges.painted = compress(colorChanges.painted);
      }
    }

    _SyncPaint__WEBPACK_IMPORTED_MODULE_3__["paintManager"].update({
      changes
    });
  }
}, 1000, {
  maxWait: 1000
});

_SyncPaint__WEBPACK_IMPORTED_MODULE_3__["paintManager"].emitter.on("update", data => {
  if (data.room_id !== "list") {
    console.log(data.room_id);
    const [surfaceId, colorId] = data.room_id.split("-");
    const mesh = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes().find(mesh => mesh.name === surfaceId);

    if (!mesh) {
      console.error("mesh not found");
      return;
    }

    Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_7__["setAnnotation"])({
      mesh,
      colorId,
      data: { ...data,
        painted: decompress(data.painted)
      }
    });
    updateMetricsOnPaintTable();
  }
});

const getCursorRadius = annotatorRadius => annotatorRadius || 0.3;

const updateCursor = position => {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor.visible === false) {
    return;
  }

  const radius = getCursorRadius(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].AnnotatorRadius);
  const cursor = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].cursor;

  if (position) {
    cursor.position.copy(position);
    const zoom = radius;
    cursor.scale.set(zoom, zoom, zoom);
    cursor.material.opacity = 0.3;
  } else {
    cursor.material.opacity = 0;
  }
};

const updateMetricsOnPaintTable = () => {
  const activeSurfaces = new Set(_SurfaceTable__WEBPACK_IMPORTED_MODULE_4__["SurfaceTable"].getData().filter(row => row.act).map(row => Object(_HandleSurfaces__WEBPACK_IMPORTED_MODULE_5__["getSurfaceName"])(row.id)));
  const meshes = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes().filter(mesh => activeSurfaces.has(mesh.name));
  const params = Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_7__["getCurrentParams"])({
    meshes
  });
  const areas = params.areas;
  const newRows = _PaintTable__WEBPACK_IMPORTED_MODULE_1__["PaintTable"].getData("active").map((item = {}) => {
    return { ...item,
      area: areas[item.id]
    };
  });
  _PaintTable__WEBPACK_IMPORTED_MODULE_1__["PaintTable"].updateData(newRows);
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
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.position.set(0, 10, 0); //default; light shining from top

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.target.position.set(0, 0, 0); //default; light shining from top

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.intensity = 0.8; //APP.camera.add( APP.directionalLight );

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight = new THREE.AmbientLight(0xffffff);
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight.intensity = 0.5;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].camera.add(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].ambientLight); // var min = 0 ;
  // var max = 255 ;
  // Controlsを用意

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

  var geometry = new THREE.SphereBufferGeometry(1, 32, 32);
  var material = new THREE.MeshLambertMaterial({
    color: 0xffffff,
    opacity: 0,
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
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerRadius = 0.1;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].MarkerID = 1; // Surface opacity

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = 1.0;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity_reserved = 0.5; // Skeleton

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode = 0; // Sphere

  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode = 0; //Boundingbox

  const call_url = location.protocol + "//" + location.host + "/surface/VolumeDescription.json";
  $.getJSON(call_url).done(function (data) {
    //data_parsed = JSON.parse(data);
    console.log(data);
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX = data.boundingbox_um.x;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY = data.boundingbox_um.y;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ = data.boundingbox_um.z;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax = Math.max(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ);
    console.log('APP.BoundingboxMax: ', _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxMax);
    window.CenterXY();
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].directionalLight.target.position.set(_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxX / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxY / 2.0, _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].BoundingboxZ / 2.0);
    window.DirLightX(false);
    window.DirLightY(false);
    window.DirLightZ(false); // https://threejsfundamentals.org/threejs/lessons/threejs-lights.html
  });
}
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../node_modules/buffer/index.js */ "./node_modules/buffer/index.js").Buffer))

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
/* harmony import */ var jsfive__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jsfive */ "./node_modules/jsfive/index.js");
/* harmony import */ var _MarkerTable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./MarkerTable */ "./js/MarkerTable.js");
/* harmony import */ var _SurfaceTable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./SurfaceTable */ "./js/SurfaceTable.js");
//
//
//
//
//




 // Change the opacity of all surface objects

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletons = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.traverse(function (obj) {
    if (obj instanceof THREE.Mesh === true && obj.visible === true && obj.name.length === 10) {
      var id = obj.name - 0;
      var col = obj.material.color;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject(id, col);
    }
  });
};

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletons = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.traverse(function (obj) {
    if (obj.name.match(/line/)) {
      obj.visible = false;
    }
  });
}; // Add stl objects and a name


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].generateSkeletons = function () {
  const call_url = location.protocol + "//" + location.host + "/ws/surface_skeleton";
  const skel_scale = document.getElementById("SkelScale");
  const skel_constant = document.getElementById("SkelConstant");
  const skel_min_voxels = document.getElementById("SkelMinVoxels");
  const skel_max_paths = document.getElementById("SkelMaxPaths");
  const skel_smoothness = document.getElementById("SkelSmoothness");
  const skel_extra_after = document.getElementsByName("SkelExtraAfter");
  var request = {};
  request["mode"] = "skeleton";
  request["scale"] = String(skel_scale.value);
  request["constant"] = String(skel_constant.value);
  request["min_voxel"] = String(skel_min_voxels.value);
  request["max_path"] = String(skel_max_paths.value);
  request["smooth"] = String(skel_smoothness.value);
  request["extra_after"] = String(skel_extra_after.value) === 'true';
  request["element"] = []; // Get JSON variable that shows the skeletons "ids and colors", and associated markers.

  var rows = _SurfaceTable__WEBPACK_IMPORTED_MODULE_4__["SurfaceTable"].searchRows("act", "=", true);

  for (var i in rows) {
    var id = rows[i].getData().id;
    var r = rows[i].getData().r;
    var g = rows[i].getData().g;
    var b = rows[i].getData().b;
    var col = r * 256 * 256 + g * 256 + b * 1; //console.log('Target id: ', id);

    var element = {};
    element.id = id;
    element.color = col; // Remove current skeleton

    var name = 'line' + ('0000000000' + id).slice(-10);
    var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

    if (obj != undefined) {
      //obj.geometry.dispose();
      //obj.material.dispose();
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.remove(obj);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].disposeNode(obj);
    } // Get marker points


    var rows_marker = _MarkerTable__WEBPACK_IMPORTED_MODULE_3__["MarkerTable"].searchRows("parentid", "=", id);
    var markerlocs = [];

    for (var j in rows_marker) {
      var id_marker = rows_marker[j].getData().id;
      var mx = rows_marker[j].getData().x;
      var my = rows_marker[j].getData().y;
      var mz = rows_marker[j].getData().z; //console.log('Marker id: ', id_marker);
      //console.log('x,y,z: ',mx,my,mz);

      markerlocs.push([mx, my, mz]);
    }

    element.markerlocs = markerlocs;
    console.log('element: ', element);
    request["element"].push(element);
  } // console.log(request)
  //Send request to Server


  var req = new XMLHttpRequest();

  req.onreadystatechange = function () {
    var READYSTATE_COMPLETED = 4;
    var HTTP_STATUS_OK = 200;

    if (this.readyState == READYSTATE_COMPLETED && this.status == HTTP_STATUS_OK) {
      // レスポンスの表示
      if (this.responseText == "False") {
        alert("No skeleton.");
        return false;
      }
    }
  };

  req.open('POST', call_url, false);
  req.setRequestHeader('Content-Type', 'application/json');
  req.send(JSON.stringify(request));

  for (const elem of request["element"]) {
    console.log("Element: ", elem);
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject(elem.id, elem.color);
  }
}; //
// Add stl objects and a name


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject = function (id, col) {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SkeletonMode == 0) {
    return false;
  }

  const call_url = location.protocol + "//" + location.host + "/ws/surface_skeleton";
  const target_url = location.protocol + "//" + location.host + "/skeleton/whole/" + ('0000000000' + id).slice(-10) + ".hdf5";
  const filename = ('0000000000' + id).slice(-10) + ".hdf5";
  const name = 'line' + ('0000000000' + id).slice(-10); // Revive if it already exists.
  // console.log('Name: ', name)

  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // console.log('Obj: ', obj)
    obj.visible = true;
    return true;
  } // Request the surface mesh generation to the server if it does not exist.


  var xhr = new XMLHttpRequest();
  xhr.open("HEAD", target_url, false); //同期モード promise method

  xhr.send(null);

  if (xhr.status == 404) {
    // alert("No skeleton.");
    console.log('No skeleton data:', id);
    return false;
  } //


  fetch(target_url).then(function (response) {
    return response.arrayBuffer();
  }).then(function (buffer) {
    //
    //
    var f = new jsfive__WEBPACK_IMPORTED_MODULE_2__["File"](buffer, filename);
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
    ////// Uncaught TypeError: Cannot read property '0' of undefined

    if (typeof data_vertices !== "object") {
      console.log('Not skeleton data.');
      return false;
    }

    if (typeof data_vertices[0] === "undefined") {
      console.log('Errornous skeleton data.');
      console.log(data_vertices);
      return false;
    }

    if (isNaN(data_vertices[0][0]) == true) {
      // console.log(data_vertices);
      console.log('Errornous skeleton data.');
      return false;
    }

    var geometry = new THREE.Geometry();
    var material = new THREE.LineBasicMaterial({
      color: col,
      //0x000000
      linewidth: 3,
      fog: true
    });

    for (let i = 0; i < data_edges.length; i++) {
      i1 = data_edges[i][0];
      i2 = data_edges[i][1]; //			console.log('Vertices ID: ', i1, i2 );
      //			console.log('data_vertices[i1]: ', data_vertices[i1] );
      //			console.log('data_vertices[i2]: ', data_vertices[i2] );

      v1 = new THREE.Vector3(data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
      v2 = new THREE.Vector3(data_vertices[i2][0], data_vertices[i2][1], data_vertices[i2][2]);
      geometry.vertices.push(v1, v2);
    }

    var line = new THREE.LineSegments(geometry, material);
    line.name = name; // console.log(line.name);

    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(line); //
    //
    //
  });
}; // Change the color of a skeleton object specified by a name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSkeletonObjectColor = function (id, col) {
  name = 'line' + ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    obj.material.color.setHex(col);
  }
}; // Remove a stl object by the name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletonObject = function (id) {
  name = 'line' + ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // APP.scene.remove(obj);
    obj.visible = false;
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

/***/ "./js/HandleSpheres.js":
/*!*****************************!*\
  !*** ./js/HandleSpheres.js ***!
  \*****************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");
/* harmony import */ var jsfive__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jsfive */ "./node_modules/jsfive/index.js");
/* harmony import */ var _SurfaceTable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./SurfaceTable */ "./js/SurfaceTable.js");
//
//
//
//
//



 // Change the opacity of all surface objects

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSpheres = function () {
  var rows = _SurfaceTable__WEBPACK_IMPORTED_MODULE_3__["SurfaceTable"].searchRows("act", "=", true);

  for (var i in rows) {
    var id = rows[i].getData().id;
    var r = rows[i].getData().r;
    var g = rows[i].getData().g;
    var b = rows[i].getData().b;
    var col = r * 256 * 256 + g * 256 + b * 1;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSphereObject(id, col);
  }
};

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSpheres = function () {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.traverse(function (obj) {
    if (obj.name.match(/Spheres/)) {
      obj.visible = false;
    }
  });
}; // Add stl objects and a name


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSphereObject = function (id, col) {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode == 0) {
    return false;
  }

  const target_url = location.protocol + "//" + location.host + "/skeleton/whole/" + ('0000000000' + id).slice(-10) + ".hdf5";
  const filename = ('0000000000' + id).slice(-10) + ".hdf5";
  const name = 'Spheres' + ('0000000000' + id).slice(-10); // Revive if it already exists.
  // console.log('Name: ', name)

  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // console.log('Obj: ', obj)
    obj.visible = true;
    return true;
  } //


  fetch(target_url).then(function (response) {
    return response.arrayBuffer();
  }).then(function (buffer) {
    //
    //
    var f = new jsfive__WEBPACK_IMPORTED_MODULE_2__["File"](buffer, filename);
    let g1 = f.get('vertices');
    let g2 = f.get('edges');
    let g3 = f.get('radiuses');
    let g4 = f.get('tangents');
    var data_vertices = g1.value;
    var data_edges = g2.value;
    var data_radiuses = g3.value;
    var data_tangents = g4.value;
    data_vertices = splitArray(data_vertices, 3);
    data_edges = splitArray(data_edges, 2);
    data_radiuses = splitArray(data_radiuses, 1);
    data_tangents = splitArray(data_tangents, 3);
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
    var spheres = new THREE.Group();

    for (var i = 0; i < data_edges.length; i++) {
      i1 = data_edges[i][0];
      i2 = data_edges[i][1]; // console.log('Vertices ID: ', i1, i2 );

      v1 = new THREE.Vector3(data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
      v2 = new THREE.Vector3(data_vertices[i2][0], data_vertices[i2][1], data_vertices[i2][2]);
      geometry.vertices.push(v1, v2); // Create circle object

      var radius = data_radiuses[i1];

      if (i1 % 10 == 1 && radius > 0.01) {
        // if ( data_vertices[i1][2] <= APP.BoundingboxZ * 0.05 ) {continue;}
        // if ( data_vertices[i1][1] <= APP.BoundingboxY * 0.05 ) {continue;}
        // if ( data_vertices[i1][0] <= APP.BoundingboxX * 0.05 ) {continue;}
        // if ( data_vertices[i1][2] >= APP.BoundingboxZ * 0.95 ) {continue;}
        // if ( data_vertices[i1][1] >= APP.BoundingboxY * 0.95 ) {continue;}
        // if ( data_vertices[i1][0] >= APP.BoundingboxX * 0.95 ) {continue;}
        // console.log(data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
        const geometry = new THREE.CircleGeometry(radius, 20);
        const material = new THREE.MeshPhongMaterial({
          color: col,
          opacity: 0.3,
          transparent: true,
          side: THREE.DoubleSide
        });
        const vertice_r = new THREE.Mesh(geometry, material);
        vertice_r.position.set(data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
        var theta_z = Math.atan(data_tangents[i1][1] / data_tangents[i1][0]);
        var theta_x = Math.acos(data_tangents[i1][2]); //vertice_r.lookAt(new THREE.Vector3(0, 0, 0));
        //vertice_r.rotation.set(rx,0,rz)

        var q = new THREE.Quaternion();
        var axis1 = new THREE.Vector3(0, 0, 1);
        var axis2 = new THREE.Vector3(data_tangents[i1][0], data_tangents[i1][1], data_tangents[i1][2]);
        q.setFromUnitVectors(axis1, axis2);
        vertice_r.quaternion.multiply(q); //vertice_r.quaternion.multiply( q );

        spheres.add(vertice_r);
      }
    }

    var line = new THREE.LineSegments(geometry, material);
    spheres.add(line);
    spheres.name = name;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(spheres); //
    //
  });
}; // Change the color of a skeleton object specified by a name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSphereObjectColor = function (id, col) {
  name = 'Spheres' + ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    obj.material.color.setHex(col);
  }
}; // Remove a stl object by the name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSphereObject = function (id) {
  name = 'Spheres' + ('0000000000' + id).slice(-10);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // APP.scene.remove(obj);
    obj.visible = false;
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
/*! exports provided: getSurfaceName */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getSurfaceName", function() { return getSurfaceName; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");
/* harmony import */ var _PaintTable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./PaintTable */ "./js/PaintTable.js");
/* harmony import */ var _SyncPaint__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./SyncPaint */ "./js/SyncPaint.js");
/* harmony import */ var _SurfaceTable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./SurfaceTable */ "./js/SurfaceTable.js");
//
//
//
//
//





const getSurfaceName = id => {
  return ('0000000000' + id).slice(-10);
}; // Add surface objects and a name

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSurfaceObject = function (id, col) {
  if (_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].SphereMode == 1) {
    return false;
  }

  const name = getSurfaceName(id);
  const call_url = location.protocol + "//" + location.host + "/ws/surface_skeleton";
  const target_url = location.protocol + "//" + location.host + "/surface/whole/" + name + ".stl"; // Revive it if already exists.
  // console.log('Name: ', name)

  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // console.log('Obj: ', obj)
    obj.visible = true;
    obj.material.opacity = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity;
    _SyncPaint__WEBPACK_IMPORTED_MODULE_3__["paintManager"].addSurface(name);
    return true;
  } // Request the surface mesh generation to the server if it does not exist.


  var xhr = new XMLHttpRequest();
  xhr.open("HEAD", target_url, false); //同期モード promise method

  xhr.send(null);

  if (xhr.status == 404) {
    // Obtain smoothing option
    const SmoothMeth = document.getElementsByName("SmoothingMethod"); // document.SmoothingMethod;

    const NumIter = document.getElementById("SmoothingNumIters"); // SmoothingNumIters;

    let Smeth = "";

    for (let i = 0; i < SmoothMeth.length; i++) {
      if (SmoothMeth[i].checked) {
        //(SmoothMeth[i].checked === true)と同じ
        Smeth = SmoothMeth[i].value;
        break;
      }
    } //Send request


    var data = {
      mode: "surface",
      id: id,
      smooth_method: Smeth,
      num_iter: String(NumIter.value)
    }; // POSTメソッドで送信するデータ

    var req = new XMLHttpRequest();

    req.onreadystatechange = function () {
      var READYSTATE_COMPLETED = 4;
      var HTTP_STATUS_OK = 200;

      if (this.readyState == READYSTATE_COMPLETED && this.status == HTTP_STATUS_OK) {
        // レスポンスの表示
        if (this.responseText == "False") {
          alert("No surface.");
          return false;
        }
      }
    };

    req.open('POST', call_url, false); // サーバに対して解析方法を指定する

    req.setRequestHeader('Content-Type', 'application/json'); // データをリクエスト ボディに含めて送信する

    req.send(JSON.stringify(data)); //
    //			以前、GET methodで
    //			var req = new XMLHttpRequest();
    //			req.open("get", call_url+id, false);
    //			req.send(null);
    //			if (req.responseText == "False") {
    //				alert("No surface.");
    //				return false;
    //				}
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
      side: THREE.DoubleSide
    }); // APP.surface_opacity

    var mesh = new THREE.Mesh(bufferGeometry, meshMaterial);
    mesh.name = name;
    mesh.scale.set(1, 1, 1); // mesh.material.side = THREE.DoubleSide;

    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.add(mesh); // console.log(mesh.name);

    Object(_PaintTable__WEBPACK_IMPORTED_MODULE_2__["updateColorOptionsOnAnnotator"])();
    _SyncPaint__WEBPACK_IMPORTED_MODULE_3__["paintManager"].addSurface(name);
  });
}; // Change the opacity of all surface objects


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectOpacity = function (opacity) {
  // console.log('Input opacity: ', opacity)
  var invisible = 0;

  if (opacity == -2) {
    invisible = 1;
  } else if (opacity == -1) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = 1;
  } else if (opacity == 0) {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity_reserved;
  } else {
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity = opacity;
    _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].surface_opacity_reserved = opacity;
  }

  ;
  var rows = _SurfaceTable__WEBPACK_IMPORTED_MODULE_4__["SurfaceTable"].searchRows("act", "=", true);

  for (var i in rows) {
    var id = rows[i].getData().id;
    var r = rows[i].getData().r;
    var g = rows[i].getData().g;
    var b = rows[i].getData().b;

    if (invisible == 1) {
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSurfaceObject(id);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletonObject(id);
    } else {
      var col = r * 256 * 256 + g * 256 + b * 1;
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSurfaceObject(id, col);
      _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSkeletonObject(id, col);
    }
  }
}; // if (obj instanceof THREE.Mesh === true && /^\d*$/.test(obj.name) && obj.name.length === 10 ) {
// Change the color of a surface object specified by the name.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].changeSurfaceObjectColor = function (id, objcolor) {
  const name = getSurfaceName(id);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    obj.material.color.setHex(objcolor);
  }
}; // Remove a stl object by a name after generation.


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSurfaceObject = function (id) {
  const name = getSurfaceName(id);
  var obj = _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].scene.getObjectByName(name);

  if (obj != undefined) {
    // APP.scene.remove(obj);
    obj.visible = false;
  }

  _SyncPaint__WEBPACK_IMPORTED_MODULE_3__["paintManager"].removeSurface(name);
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
/* harmony import */ var tabulator_tables__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! tabulator-tables */ "./node_modules/tabulator-tables/dist/js/tabulator.js");
/* harmony import */ var tabulator_tables__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(tabulator_tables__WEBPACK_IMPORTED_MODULE_2__);



const MarkerTable = new tabulator_tables__WEBPACK_IMPORTED_MODULE_2__("#MarkerTable", {
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
      min: 0.01,
      max: 1,
      step: 0.01
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

    var markers = replaceColumnTitle(MarkerTable, parsedData); // 同じ座標のためスキップした数

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
  return MarkerTable.getDataCount() === 0;
}
/**
 * MarkerTableをクリアする
 */


function clearMarkerTable() {
  var rows = MarkerTable.getRows();
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
  var rows = MarkerTable.getRows();
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

/***/ "./js/PaintTable.js":
/*!**************************!*\
  !*** ./js/PaintTable.js ***!
  \**************************/
/*! exports provided: updateColorOptionsOnAnnotator, PaintTable */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "updateColorOptionsOnAnnotator", function() { return updateColorOptionsOnAnnotator; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PaintTable", function() { return PaintTable; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _SyncPaint__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./SyncPaint */ "./js/SyncPaint.js");
/* harmony import */ var _three_annotator_index__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./three_annotator/index */ "./js/three_annotator/index.js");
/* harmony import */ var tabulator_tables__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! tabulator-tables */ "./node_modules/tabulator-tables/dist/js/tabulator.js");
/* harmony import */ var tabulator_tables__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(tabulator_tables__WEBPACK_IMPORTED_MODULE_3__);





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
  Object(_SyncPaint__WEBPACK_IMPORTED_MODULE_1__["updatePaintObservation"])();
  const activeColors = [];
  const colorParams = {
    eraser: {
      r: 1,
      g: 1,
      b: 1
    }
  };
  const tableData = PaintTable.getData("active");
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
    eraser: !_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_on,
    overwrite: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_overwriteB
  };
  Object(_three_annotator_index__WEBPACK_IMPORTED_MODULE_2__["setColorOptions"])(colorOptions, {
    meshes: _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].getMeshes()
  });
};
const PaintTable = new tabulator_tables__WEBPACK_IMPORTED_MODULE_3__('#PaintTable', {
  layout: "fitColumns",
  autoResize: true,
  responsiveLayout: "hide",
  tooltips: true,
  addRowPos: "top",
  history: true,
  pagination: "local",
  paginationSize: 10,
  resizableRows: true,
  movableRows: true,
  initialSort: [],
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
      updateMetricsOnPaintTable();
    }
  }, {
    title: "Target",
    field: "target",
    width: 73,
    hozAlign: "center",
    formatter: "tickCross",
    headerSort: false,
    cellClick: (e, cell) => {
      const table = PaintTable;
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
    width: 40,
    headerSort: false
  }, {
    title: "Name",
    field: "name",
    editor: "input",
    headerSort: false,
    cellEdited: () => updateColor()
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
    headerSort: false,
    cellEdited: () => updateColor()
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
    headerSort: false,
    cellEdited: () => updateColor()
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
    headerSort: false,
    cellEdited: () => updateColor()
  }, {
    title: "Area",
    field: "area",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    }
  }, {
    title: "Volume",
    field: "volume",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    }
  }, {
    title: "Area reserv",
    field: "area_reserv",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    },
    visible: false
  }, {
    title: "Length",
    field: "length",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    },
    visible: false
  }, {
    title: "Max r",
    field: "max_radius",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    },
    visible: false
  }, {
    title: "Mean r",
    field: "max_radius",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    },
    visible: false
  }, {
    title: "Min r",
    field: "min_radius",
    headerSort: false,
    formatter: "money",
    formatterParams: {
      precision: 5
    },
    visible: false
  }],
  rowMoved: row => {
    updateColor();
  },
  rowDeleted: row => {
    updateColor();
  },
  rowAdded: row => {
    updateColor();
  }
});

const updateColor = () => {
  updateColorOptionsOnAnnotator();
  _SyncPaint__WEBPACK_IMPORTED_MODULE_1__["paintManager"].updateList({
    list: PaintTable.getData(),
    lastPaintId
  });
};

window.switchAnnotation = checked => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_mode = checked;
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].controls.noRotate = checked;
};

window.switchEraserAnnotation = checked => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_on = checked;
  updateColorOptionsOnAnnotator();
};

window.setAnnotationOverwrite = checked => {
  _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].paint_overwriteB = checked;
  updateColorOptionsOnAnnotator();
};

let lastPaintId = 0;
$('#button-add-paint-layer').on('click', event => {
  lastPaintId++;
  const hasTarget = PaintTable.getData("active").some(item => item.target);
  var layer = Object.assign({
    id: lastPaintId,
    name: "Layer" + String(lastPaintId),
    area: 0,
    volume: 0,
    visibility: true,
    target: !hasTarget
  }, getRandomColor(lastPaintId));
  PaintTable.addData(layer);
  updateColorOptionsOnAnnotator();
});
$('#save-paint-table-csv').on('click', event => {
  downloadPaintTableAsCSV();
}); //// 201016

$('#calc-volumes').on('click', event => {
  _SyncPaint__WEBPACK_IMPORTED_MODULE_1__["paintManager"].updatePaintVolumes();
}); //// 211223

const downloadPaintTableAsCSV = () => {
  const tableData = PaintTable.getData("active");
  const csvData = [["id", "name", "r", "g", "b", "area", "volume", "area_reserv", "length", "max_radius", "mean_radius", "min_radius"]];

  for (const row of tableData) {
    csvData.push([row.id, row.name, row.r, row.g, row.b, row.area, row.volume, row.area_reserv, row.length, row.max_radius, row.mean_radius, row.min_radius]);
  }
  /*
    const csvData = [["id", "name", "r", "g", "b", "area", "volume"]]
    for (const row of tableData) {
      csvData.push([row.id, row.name, row.r, row.g, row.b, row.area, row.volume]);
    }
  */


  const csvContent = "data:text/csv;charset=utf-8," + csvData.map(e => e.join(",")).join("\n");
  const encodeUri = encodeURI(csvContent); // window.open(encodeUri); This also download CSV file

  const link = document.createElement("a");
  link.setAttribute("href", encodeUri);
  link.setAttribute("download", "paint.csv");
  document.body.appendChild(link);
  link.click();
};

const syncSequence = true;
_SyncPaint__WEBPACK_IMPORTED_MODULE_1__["paintManager"].emitter.on("update", data => {
  if (data.room_id === "list") {
    const currentRows = PaintTable.getData() || [];
    const incomingRows = data.list || [];
    console.log(incomingRows);

    if (syncSequence) {
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
          min_radius: incomingRow.min_radius
        };
      }));
    } else {
      const incomingRowsMap = new Map(incomingRows.map(incomingRow => [incomingRow.id, incomingRow]));
      const newRows = [];

      for (const currentRow of currentRows) {
        if (incomingRowsMap.has(currentRow.id)) {
          const incomingRow = incomingRowsMap.get(currentRow.id);
          newRows.push({ ...currentRow,
            name: incomingRow.name,
            r: incomingRow.r,
            g: incomingRow.g,
            b: incomingRow.b,
            volume: incomingRow.volume,
            area_reserv: incomingRow.area_reserv,
            length: incomingRow.length,
            max_radius: incomingRow.max_radius,
            mean_radius: incomingRow.mean_radius,
            min_radius: incomingRow.min_radius
          });
          incomingRowsMap.delete(currentRow.id);
        }
      }

      for (const [id, incomingRow] of incomingRowsMap) {
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
          min_radius: incomingRow.min_radius
        });
      }

      PaintTable.setData(newRows);
    }

    lastPaintId = data.lastPaintId || 0;
    updateColorOptionsOnAnnotator();
  }
});

/***/ }),

/***/ "./js/SurfaceTable.js":
/*!****************************!*\
  !*** ./js/SurfaceTable.js ***!
  \****************************/
/*! exports provided: SurfaceTable */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SurfaceTable", function() { return SurfaceTable; });
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
/* harmony import */ var _csv__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./csv */ "./js/csv.js");
/* harmony import */ var _HandleBasement__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./HandleBasement */ "./js/HandleBasement.js");
/* harmony import */ var tabulator_tables__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! tabulator-tables */ "./node_modules/tabulator-tables/dist/js/tabulator.js");
/* harmony import */ var tabulator_tables__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(tabulator_tables__WEBPACK_IMPORTED_MODULE_3__);




const SurfaceTable = new tabulator_tables__WEBPACK_IMPORTED_MODULE_3__("#SurfaceTable", {
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
        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].addSphereObject(id, col);
      }

      if (act == false) {
        console.log("Disappear ID:", id); //const filename = sprintf("./stls/i%d.stl", id );

        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSurfaceObject(id);
        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSkeletonObject(id);
        _APP__WEBPACK_IMPORTED_MODULE_0__["APP"].removeSphereObject(id);
      }

      Object(_HandleBasement__WEBPACK_IMPORTED_MODULE_2__["updateMetricsOnPaintTable"])();
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

/***/ "./js/SyncPaint.js":
/*!*************************!*\
  !*** ./js/SyncPaint.js ***!
  \*************************/
/*! exports provided: socket, paintManager, updatePaintObservation */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "socket", function() { return socket; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "paintManager", function() { return paintManager; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "updatePaintObservation", function() { return updatePaintObservation; });
/* harmony import */ var _PaintTable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./PaintTable */ "./js/PaintTable.js");
/* harmony import */ var _SurfaceTable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./SurfaceTable */ "./js/SurfaceTable.js");
/* harmony import */ var crypto__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! crypto */ "./node_modules/crypto-browserify/index.js");
/* harmony import */ var crypto__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(crypto__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var events__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! events */ "./node_modules/events/events.js");
/* harmony import */ var events__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(events__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var socket_io_client__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! socket.io-client */ "./node_modules/socket.io-client/lib/index.js");
/* harmony import */ var socket_io_client__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(socket_io_client__WEBPACK_IMPORTED_MODULE_4__);





const socket = socket_io_client__WEBPACK_IMPORTED_MODULE_4___default()(`${location.origin}/`);
socket.on('system', data => {
  console.log('system', data);
});

const subtract = function* (a, b) {
  for (const item of a) {
    if (!b.has(item)) {
      yield item;
    }
  }
};

class RoomManager {
  constructor(socket) {
    this.values = new Map();
    this.emitter = new events__WEBPACK_IMPORTED_MODULE_3___default.a();

    this.onUpdateData = data => {
      const currentData = this.values.get(data.room_id);

      if (!currentData || (currentData.sid || this.socket.id) !== this.socket.id || data.sid !== this.socket.id) {
        this.values.set(data.room_id, data);
        this.emitter.emit("update", data);
      }
    };

    this.socket = socket;
    this.socket.on('update', this.onUpdateData);
    this.socket.on('current', this.onUpdateData);
  }

  enterRoom(roomId) {
    this.socket.emit("enter", roomId);
  }

  leaveRoom(roomId) {
    this.socket.emit("leave", roomId);
    this.values.delete(roomId);
  }

}

class PaintManager extends RoomManager {
  constructor(...args) {
    super(...args);
    this.colors = new Set();
    this.surfaces = new Set();
  }

  getRoomId({
    surface,
    color
  }) {
    return `${surface}-${color}`;
  }

  addColor(color) {
    for (const surface of this.surfaces) {
      this.enterRoom(this.getRoomId({
        color,
        surface
      }));
    }

    this.colors.add(color);
  }

  removeColor(color) {
    for (const surface of this.surfaces) {
      this.leaveRoom(this.getRoomId({
        color,
        surface
      }));
    }

    this.colors.delete(color);
  }

  addSurface(surface) {
    for (const color of this.colors) {
      this.enterRoom(this.getRoomId({
        color,
        surface
      }));
    }

    this.surfaces.add(surface);
  }

  removeSurface(surface) {
    for (const color of this.colors) {
      this.leaveRoom(this.getRoomId({
        color,
        surface
      }));
    }

    this.surfaces.delete(surface);
  }

  update(data) {
    for (const [objectId, objectData] of Object.entries(data.changes)) {
      for (const [colorId, colorData] of Object.entries(objectData)) {
        const roomId = objectId + "-" + colorId;
        this.values.set(roomId, colorData);
      }
    }

    this.socket.emit("update_paint", data);
  } // 200116 HU


  updatePaintVolumes() {
    this.socket.emit("update_paint_volumes");
  } //


  updateList({
    list,
    lastPaintId
  }) {
    this.socket.emit("update", {
      list,
      lastPaintId,
      room_id: "list"
    });
  }

}

const paintManager = new PaintManager(socket);
let oldActiveColors = new Set();
const updatePaintObservation = () => {
  const activeColors = new Set();
  const tableData = _PaintTable__WEBPACK_IMPORTED_MODULE_0__["PaintTable"].getData("active");

  for (const row of tableData) {
    if (row.visibility) {
      activeColors.add(row.id);
    }
  }

  for (const item of subtract(oldActiveColors, activeColors)) {
    paintManager.removeColor(item);
  }

  for (const item of subtract(activeColors, oldActiveColors)) {
    paintManager.addColor(item);
  }

  oldActiveColors = activeColors;
};

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
/* harmony import */ var _js_SurfaceTable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../js/SurfaceTable */ "./js/SurfaceTable.js");
/* harmony import */ var _js_HandleSurfaces__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../js/HandleSurfaces */ "./js/HandleSurfaces.js");
/* harmony import */ var _js_HandleSkeletons__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../js/HandleSkeletons */ "./js/HandleSkeletons.js");
/* harmony import */ var _js_HandleSpheres__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../js/HandleSpheres */ "./js/HandleSpheres.js");
/* harmony import */ var _js_HandleMarkers__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../js/HandleMarkers */ "./js/HandleMarkers.js");
/* harmony import */ var _js_SyncPaint__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../js/SyncPaint */ "./js/SyncPaint.js");
/* harmony import */ var _js_three_annotator_index__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../js/three_annotator/index */ "./js/three_annotator/index.js");
/* harmony import */ var _js_three_annotator_geometryState__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../js/three_annotator/geometryState */ "./js/three_annotator/geometryState.js");
/* harmony import */ var _js_HandleBasement__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../js/HandleBasement */ "./js/HandleBasement.js");













Object(_js_HandleBasement__WEBPACK_IMPORTED_MODULE_12__["launchAnnotator"])();

/***/ }),

/***/ "./js/three_annotator/geometryState.js":
/*!*********************************************!*\
  !*** ./js/three_annotator/geometryState.js ***!
  \*********************************************/
/*! exports provided: getGeometryState */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getGeometryState", function() { return getGeometryState; });
class GeometryColor {
  constructor(length) {
    this.painted = new Int8Array(length);
    this.totalArea = 0;
    this.updated = false;
  }

  clear() {
    this.painted.fill(0);
    this.totalArea = 0;
  }

}

class GeometryState {
  constructor(geometry) {
    this.totalArea = 0;
    this.geometryColors = {};
    this.activeColors = [0, 1, 2];
    this.targetColorId = 0;
    this.colorParams = {
      0: {
        r: 1,
        g: 0,
        b: 0
      },
      1: {
        r: 0,
        g: 1,
        b: 0
      },
      2: {
        r: 0,
        g: 0,
        b: 1
      },
      eraser: {
        r: 1,
        g: 1,
        b: 1
      }
    };
    this.eraserColorId = "eraser";
    this.overwrite = true;
    this.geometry = geometry;
    this.initArea();
  }

  initArea() {
    const vertexCount = this.geometry.attributes.position.count;
    const faceCount = vertexCount / 3;
    this.areas = new Float32Array(faceCount);
    const positionArray = this.geometry.attributes.position.array;
    const length = positionArray.length;

    for (let i = 0; i < length; i += 9) {
      const face_area = calcArea(positionArray[i + 0], positionArray[i + 1], positionArray[i + 2], positionArray[i + 3], positionArray[i + 4], positionArray[i + 5], positionArray[i + 6], positionArray[i + 7], positionArray[i + 8]);
      this.areas[i / 9] = face_area / 3;
    }
  }

  getChanges() {
    const response = {};

    for (const colorId of this.activeColors) {
      const geometryColor = this.geometryColors[colorId];

      if (geometryColor === null || geometryColor === void 0 ? void 0 : geometryColor.updated) {
        response[colorId] = {
          painted: geometryColor.painted,
          totalArea: geometryColor.totalArea
        };
        geometryColor.updated = false;
      }
    }

    return response;
  }

  setAnnotation(colorId, data) {
    const geometryColor = this.getGeometryColor(colorId);

    if (data.painted) {
      geometryColor.painted = data.painted;
      geometryColor.totalArea = data.totalArea;
      this.updateAllColor();
    }
  }

  getGeometryColor(colorId) {
    if (!this.geometryColors[colorId]) {
      const vertexCount = this.geometry.attributes.position.count;
      this.geometryColors[colorId] = new GeometryColor(vertexCount);
    }

    return this.geometryColors[colorId];
  }

  updateAllColor() {
    const colorArray = this.geometry.attributes.color.array;
    const vertexCount = colorArray.length / 3;

    for (let i = 0; i < vertexCount; i += 1) {
      this.updateColor(i);
    }

    this.geometry.attributes.color.needsUpdate = true;
    this.geometry.colorsNeedUpdate = true;
  }

  updateColor(vertexIndex) {
    let effecientColorId = this.eraserColorId;

    for (const colorId of this.activeColors) {
      var _this$geometryColors$;

      if ((_this$geometryColors$ = this.geometryColors[colorId]) === null || _this$geometryColors$ === void 0 ? void 0 : _this$geometryColors$.painted[vertexIndex]) {
        effecientColorId = colorId;
        break;
      }
    }

    const colorArray = this.geometry.attributes.color.array;
    const colorParam = this.colorParams[effecientColorId];
    colorArray[vertexIndex * 3 + 0] = colorParam.r;
    colorArray[vertexIndex * 3 + 1] = colorParam.g;
    colorArray[vertexIndex * 3 + 2] = colorParam.b;
  } //////////////


  getColorId(vertexIndex) {
    var ids = [];

    for (const colorId of this.activeColors) {
      const geometryColor = this.getGeometryColor(colorId);

      if (geometryColor.painted[vertexIndex] == 1) {
        ids.push(colorId);
      }
    }

    return ids;
  } //////////////


  setColor(vertexIndex) {
    if (this.overwrite) {
      for (const colorId of this.activeColors) {
        const geometryColor = this.getGeometryColor(colorId);

        if (colorId === this.targetColorId) {
          if (geometryColor.painted[vertexIndex] === 0) {
            geometryColor.painted[vertexIndex] = 1;
            geometryColor.totalArea += this.areas[Math.floor(vertexIndex / 3)];
            geometryColor.updated = true;
          }
        } else {
          if (geometryColor.painted[vertexIndex] === 1) {
            geometryColor.painted[vertexIndex] = 0;
            geometryColor.totalArea -= this.areas[Math.floor(vertexIndex / 3)];
            geometryColor.updated = true;
          }
        }
      }

      const colorArray = this.geometry.attributes.color.array;
      const colorParam = this.colorParams[this.eraser ? this.eraserColorId : this.targetColorId];
      colorArray[vertexIndex * 3 + 0] = colorParam.r;
      colorArray[vertexIndex * 3 + 1] = colorParam.g;
      colorArray[vertexIndex * 3 + 2] = colorParam.b;
      return true;
    } else if (this.eraser) {
      const geometryColor = this.getGeometryColor(this.targetColorId);

      if (geometryColor.painted[vertexIndex] === 1) {
        geometryColor.painted[vertexIndex] = 0;
        geometryColor.totalArea -= this.areas[Math.floor(vertexIndex / 3)];
        geometryColor.updated = true;
        this.updateColor(vertexIndex);
        return true;
      }
    } else {
      const geometryColor = this.getGeometryColor(this.targetColorId);

      if (geometryColor.painted[vertexIndex] === 0) {
        geometryColor.painted[vertexIndex] = 1;
        geometryColor.totalArea += this.areas[Math.floor(vertexIndex / 3)];
        geometryColor.updated = true;
        this.updateColor(vertexIndex);
        return true;
      }
    }
  }

  setColorOptions({
    targetColorId,
    activeColors,
    colorParams,
    eraserColorId,
    eraser,
    overwrite
  }) {
    this.activeColors = activeColors || this.activeColors;
    this.eraserColorId = eraserColorId || this.eraserColorId;
    this.colorParams = colorParams || this.colorParams;
    this.eraser = eraser != null ? eraser : this.eraser;
    this.overwrite = overwrite != null ? overwrite : this.overwrite;
    this.targetColorId = this.eraser && this.overwrite ? this.eraserColorId : this.activeColors[0];
    this.updateAllColor();
  }

  setColorParams(colorParams) {
    this.colorParams = colorParams;
    this.updateAllColor();
  }

  annotate({
    center,
    direction,
    limit,
    ignoreBackFace
  }) {
    window.geometryState = this;
    const geometry = this.geometry;
    const center_x = center.x,
          center_y = center.y,
          center_z = center.z;
    const direction_x = direction.x,
          direction_y = direction.y,
          direction_z = direction.z;
    let needsUpdate = false;

    if (geometry.isBufferGeometry) {
      const positionArray = geometry.attributes.position.array;
      const normalArray = geometry.attributes.normal.array;
      const length = positionArray.length;

      for (let i = 0; i < length; i += 3) {
        const x = positionArray[i + 0] - center_x;
        const y = positionArray[i + 1] - center_y;
        const z = positionArray[i + 2] - center_z;

        if (x * x + y * y + z * z > limit) {
          continue;
        }

        if (ignoreBackFace) {
          if (normalArray[i + 0] * direction_x + normalArray[i + 1] * direction_y + normalArray[i + 2] * direction_z < 0) {
            continue;
          }
        }

        const hasUpdated = this.setColor(i / 3);

        if (hasUpdated) {
          needsUpdate = true;
        }
      }

      if (needsUpdate) {
        geometry.attributes.color.needsUpdate = true;
        geometry.colorsNeedUpdate = true;
        return true;
      }
    }
  } ///////////////////////////


  getPaintID(center) {
    //window.geometryState = this;
    const geometry = this.geometry;
    const center_x = center.x,
          center_y = center.y,
          center_z = center.z;
    const positionArray = geometry.attributes.position.array;
    const length = positionArray.length;
    var x = positionArray[0] - center_x;
    var y = positionArray[1] - center_y;
    var z = positionArray[2] - center_z;
    var dist = x * x + y * y + z * z;
    var i_min = 0;

    for (let i = 0 + 3; i < length; i += 3) {
      x = positionArray[i + 0] - center_x;
      y = positionArray[i + 1] - center_y;
      z = positionArray[i + 2] - center_z;
      const d = x * x + y * y + z * z;

      if (d < dist) {
        i_min = i;
        dist = d;
      }
    }

    const ids = this.getColorId(i_min / 3);
    return ids;
  } ///////////////////////////


  getCurrentParams() {
    let area = 0;
    const areas = Object.keys(this.geometryColors).map(colorId => {
      var _this$geometryColors$2;

      const partArea = (_this$geometryColors$2 = this.geometryColors[colorId]) === null || _this$geometryColors$2 === void 0 ? void 0 : _this$geometryColors$2.totalArea;
      area += partArea;
      return {
        colorId,
        area: partArea
      };
    });
    return {
      area,
      areas
    };
  }

}

class GeometryStateMap {
  constructor() {
    this.map = new WeakMap();
  }

  get(geometry) {
    if (!this.map.has(geometry)) {
      this.map.set(geometry, new GeometryState(geometry));
    }

    return this.map.get(geometry);
  }

}

const geometryStateMap = new GeometryStateMap();
const getGeometryState = geometry => geometryStateMap.get(geometry);

const calcArea = (x1, y1, z1, x2, y2, z2, x3, y3, z3) => {
  const a1 = x1 - x3;
  const b1 = y1 - y3;
  const c1 = z1 - z3;
  const a2 = x2 - x3;
  const b2 = y2 - y3;
  const c2 = z2 - z3;
  const p1 = b1 * c2 - b2 * c1;
  const p2 = c1 * a2 - c2 * a1;
  const p3 = a1 * b2 - a2 * b1;
  return (p1 * p1 + p2 * p2 + p3 * p3) / 2;
};

/***/ }),

/***/ "./js/three_annotator/index.js":
/*!*************************************!*\
  !*** ./js/three_annotator/index.js ***!
  \*************************************/
/*! exports provided: getIntersect, annotateBySphere, getPaintID, getCurrentParams, setColorOptions, getChanges, setAnnotation */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getIntersect", function() { return getIntersect; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "annotateBySphere", function() { return annotateBySphere; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getPaintID", function() { return getPaintID; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getCurrentParams", function() { return getCurrentParams; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "setColorOptions", function() { return setColorOptions; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getChanges", function() { return getChanges; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "setAnnotation", function() { return setAnnotation; });
/* harmony import */ var _geometryState__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./geometryState */ "./js/three_annotator/geometryState.js");


const getRay = ({
  raymouse,
  camera
}) => {
  if (camera && camera.isPerspectiveCamera) {
    return new THREE.Vector3().set(raymouse.x, raymouse.y, 0).unproject(camera).sub(camera.position).normalize();
  } else {
    console.error("Unsupported camera type.");
  }
};

const raycaster = new THREE.Raycaster();

const _getIntersect = ({
  raymouse,
  camera,
  meshes
}) => {
  raycaster.setFromCamera(raymouse, camera);
  const intersects = raycaster.intersectObjects(meshes);
  const intersect = intersects.find(intersect => intersect.object.type === "Mesh");
  return intersect;
};

const getIntersect = ({
  x,
  y,
  camera,
  meshes,
  container
}) => {
  const raymouse = new THREE.Vector2(x / container.clientWidth * 2 - 1, -(y / container.clientHeight) * 2 + 1);

  const intersect = _getIntersect({
    raymouse,
    camera,
    meshes
  });

  return {
    intersect
  };
};
const annotateBySphere = ({
  x,
  y,
  camera,
  meshes,
  container,
  radius,
  ignoreBackFace,
  color
}) => {
  const raymouse = new THREE.Vector2(x / container.clientWidth * 2 - 1, -(y / container.clientHeight) * 2 + 1);

  const intersect = _getIntersect({
    raymouse,
    camera,
    meshes
  });

  if (!intersect) {
    return {
      intersect
    };
  }

  const mesh = intersect.object;
  const geometry = mesh.geometry; // 高速化のため、逆行列をかけておく

  const center = intersect.point.clone().applyMatrix4(new THREE.Matrix4().getInverse(mesh.matrix));
  const scale = mesh.scale.x; // scale.x, scale.y, scale.z are the same

  const limit = radius * radius / (scale * scale);
  const direction = getRay({
    raymouse,
    camera
  });
  const geometryState = Object(_geometryState__WEBPACK_IMPORTED_MODULE_0__["getGeometryState"])(geometry);
  geometryState.annotate({
    center,
    direction,
    limit,
    color,
    ignoreBackFace
  });
  return {
    intersect
  };
}; ///////////////////////////////

const getPaintID = ({
  x,
  y,
  camera,
  meshes,
  container
}) => {
  const raymouse = new THREE.Vector2(x / container.clientWidth * 2 - 1, -(y / container.clientHeight) * 2 + 1);

  const intersect = _getIntersect({
    raymouse,
    camera,
    meshes
  });

  if (!intersect) {
    return {
      intersect
    };
  }

  const mesh = intersect.object;
  const geometry = mesh.geometry; // 高速化のため、逆行列をかけておく

  const center = intersect.point.clone().applyMatrix4(new THREE.Matrix4().getInverse(mesh.matrix)); //  const scale = mesh.scale.x; // scale.x, scale.y, scale.z are the same
  //  const limit = (radius * radius) / (scale * scale);
  //  const direction = getRay({ raymouse, camera });

  const geometryState = Object(_geometryState__WEBPACK_IMPORTED_MODULE_0__["getGeometryState"])(geometry);
  const ids = geometryState.getPaintID(center);
  return ids;
}; ///////////////////////////////

const getCurrentParams = ({
  meshes
}) => {
  let area = 0;
  const areas = {};
  meshes.forEach(mesh => {
    const geometry = mesh.geometry;

    if (!geometry.isBufferGeometry) {
      return;
    }

    const geometryState = Object(_geometryState__WEBPACK_IMPORTED_MODULE_0__["getGeometryState"])(geometry);
    const result = geometryState.getCurrentParams();
    area += result.area;
    result.areas.forEach(o => {
      areas[o.colorId] = (areas[o.colorId] || 0) + o.area;
    });
  });
  return {
    area,
    areas
  };
};
const setColorOptions = (options, {
  meshes
}) => {
  meshes.forEach(mesh => {
    const geometry = mesh.geometry;

    if (!geometry.isBufferGeometry) {
      return;
    }

    const geometryState = Object(_geometryState__WEBPACK_IMPORTED_MODULE_0__["getGeometryState"])(geometry);
    geometryState.setColorOptions(options);
  });
};
const getChanges = ({
  meshes
}) => {
  const response = {};
  meshes.forEach(mesh => {
    const geometry = mesh.geometry;

    if (!geometry.isBufferGeometry) {
      return;
    }

    const geometryState = Object(_geometryState__WEBPACK_IMPORTED_MODULE_0__["getGeometryState"])(geometry);
    const changes = geometryState.getChanges();

    if (Object.keys(changes).length > 0) {
      response[mesh.name] = changes;
    }
  });
  return response;
};
const setAnnotation = ({
  mesh,
  colorId,
  data
}) => {
  const geometry = mesh.geometry;
  const geometryState = Object(_geometryState__WEBPACK_IMPORTED_MODULE_0__["getGeometryState"])(geometry);
  geometryState.setAnnotation(colorId, data);
};

/***/ }),

/***/ "./js/util.js":
/*!********************!*\
  !*** ./js/util.js ***!
  \********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _APP__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./APP */ "./js/APP.js");
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

_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].disposeNode = function (node) {
  if (node instanceof THREE.Mesh) {
    if (node.geometry) {
      node.geometry.dispose();
    }

    if (node.material) {
      if (node.material instanceof THREE.MeshFaceMaterial) {
        $.each(node.material.materials, function (idx, mtrl) {
          if (mtrl.map) mtrl.map.dispose();
          if (mtrl.lightMap) mtrl.lightMap.dispose();
          if (mtrl.bumpMap) mtrl.bumpMap.dispose();
          if (mtrl.normalMap) mtrl.normalMap.dispose();
          if (mtrl.specularMap) mtrl.specularMap.dispose();
          if (mtrl.envMap) mtrl.envMap.dispose();
          if (mtrl.alphaMap) mtrl.alphaMap.dispose();
          if (mtrl.aoMap) mtrl.aoMap.dispose();
          if (mtrl.displacementMap) mtrl.displacementMap.dispose();
          if (mtrl.emissiveMap) mtrl.emissiveMap.dispose();
          if (mtrl.gradientMap) mtrl.gradientMap.dispose();
          if (mtrl.metalnessMap) mtrl.metalnessMap.dispose();
          if (mtrl.roughnessMap) mtrl.roughnessMap.dispose();
          mtrl.dispose(); // disposes any programs associated with the material
        });
      } else {
        if (node.material.map) node.material.map.dispose();
        if (node.material.lightMap) node.material.lightMap.dispose();
        if (node.material.bumpMap) node.material.bumpMap.dispose();
        if (node.material.normalMap) node.material.normalMap.dispose();
        if (node.material.specularMap) node.material.specularMap.dispose();
        if (node.material.envMap) node.material.envMap.dispose();
        if (node.material.alphaMap) node.material.alphaMap.dispose();
        if (node.material.aoMap) node.material.aoMap.dispose();
        if (node.material.displacementMap) node.material.displacementMap.dispose();
        if (node.material.emissiveMap) node.material.emissiveMap.dispose();
        if (node.material.gradientMap) node.material.gradientMap.dispose();
        if (node.material.metalnessMap) node.material.metalnessMap.dispose();
        if (node.material.roughnessMap) node.material.roughnessMap.dispose();
        node.material.dispose(); // disposes any programs associated with the material
      }
    }
  }
}; // disposeNode


_APP__WEBPACK_IMPORTED_MODULE_0__["APP"].disposeHierarchy = function (node, callback) {
  for (var i = node.children.length - 1; i >= 0; i--) {
    var child = node.children[i];
    disposeHierarchy(child, callback);
    callback(child);
  }
};

/***/ }),

/***/ 1:
/*!**********************!*\
  !*** util (ignored) ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports) {

/* (ignored) */

/***/ }),

/***/ 2:
/*!**********************!*\
  !*** util (ignored) ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports) {

/* (ignored) */

/***/ }),

/***/ 3:
/*!************************!*\
  !*** buffer (ignored) ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

/* (ignored) */

/***/ }),

/***/ 4:
/*!************************!*\
  !*** crypto (ignored) ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

/* (ignored) */

/***/ }),

/***/ 5:
/*!********************!*\
  !*** ws (ignored) ***!
  \********************/
/*! no static exports found */
/***/ (function(module, exports) {

/* (ignored) */

/***/ })

}]);
//# sourceMappingURL=1.bundle.js.map