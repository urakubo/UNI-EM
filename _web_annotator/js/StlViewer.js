import { AnnotationTable, updateColorOptionsOnAnnotator } from "./AnnotationTable";
import { APP } from "./APP";
import { ObjMarkerTable } from "./MarkerTable";

var xratio = 0.6;
var yratio = 0.95;
//var ysize = 600;

var frustumSize = 1000;
var xshift = -64;
var yshift = -128-59;
var zshift = -64

xshift = 0;
yshift = 0;
zshift = 0;

APP.animate = function() {
	APP.renderer.render( APP.scene, APP.camera );
	APP.controls.update();
	requestAnimationFrame( APP.animate );
};

APP.dragging = false;
APP.annotation_mode = false;
APP.annotation_paint_mode = true;
APP.annotation_overwrite = false;

// ObtainWindowSize
function onWindowResize() {
    var aspect = window.innerWidth / window.innerHeight;
    APP.camera.left   = - frustumSize * aspect / 2;
    APP.camera.right  =   frustumSize * aspect / 2;
    APP.camera.top    =   frustumSize / 2;
    APP.camera.bottom = - frustumSize / 2;
    APP.camera.updateProjectionMatrix();
    APP.renderer.setSize( window.innerWidth * xratio, window.innerHeight * yratio);
	}

// Add stl objects and a name
APP.addSTLObject = function(url, name, objcolor) {
  var loader = new THREE.STLLoader();
  loader.load(url, function(bufferGeometry) {
	  if (bufferGeometry.isBufferGeometry) {
		  bufferGeometry.attributes.color = bufferGeometry.attributes.color || bufferGeometry.attributes.position.clone();
		  bufferGeometry.attributes.color.array.fill(1);
		  bufferGeometry.attributes.color.needsUpdate = true;
		  bufferGeometry.colorsNeedUpdate = true;
	  }
	  const meshMaterial = new THREE.MeshPhongMaterial({
		  color: objcolor,
		  specular: 0x776666,
		  shininess: 0.2,
		  vertexColors: THREE.FaceColors,
		  side: true
	  })
	  var mesh = new THREE.Mesh(bufferGeometry, meshMaterial);
      mesh.name = name;
      mesh.scale.set(1, 1, 1);
      mesh.material.side = THREE.DoubleSide;
      APP.scene.add(mesh);

      mesh.translateX(xshift);
      mesh.translateY(yshift);
	  mesh.translateZ(zshift);

	  updateColorOptionsOnAnnotator();

      //APP.scene.getObjectByName('test_name2').rotation.x += 0.005;
      //APP.scene.getObjectByName('test_name2').rotation.y += 0.005;
      //console.log('Object name:');
      //console.log(name);
      //APP.scene.remove(mesh);
  });
}

// Change the color of the stl object specified by a name after generation.
APP.changecolorSTLObject = function(name, objcolor){
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	}

// Remove a stl object by a name after generation.
APP.removeSTLObject = function(name){
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
		}
	}

// Draw bounding box
APP.addBoundingBox = function(){

	if ( APP.BackGroundColor == 'Black'){
		  var mat = new THREE.LineBasicMaterial( { color: 0xFFFFFF, linewidth: 2 } );
		  }
	else{
		var mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
		}

	var geometry = new THREE.BoxBufferGeometry( APP.BoundingboxZ, APP.BoundingboxY, APP.BoundingboxX );
	var geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )

	var boundingbox = new THREE.LineSegments( geo, mat );
	boundingbox.name = 'BoundingBox';
	boundingbox.scale.set(1,1,1);
	APP.scene.add(boundingbox);
	APP.BoundingBox = 'On';
	boundingbox.translateX( APP.BoundingboxZ / 2 );
	boundingbox.translateY( APP.BoundingboxY / 2 );
	boundingbox.translateZ( APP.BoundingboxX / 2 );
	}

APP.removeBoundingBox = function(){
	var obj = APP.scene.getObjectByName('BoundingBox');
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
		}
	APP.BoundingBox = 'Off';
	}

APP.setBoundingBoxColor = function(objcolor){
	var obj = APP.scene.getObjectByName('BoundingBox');
	if ( obj != undefined ) {
    	obj.material.color.setHex( objcolor );
		}
	}

// Set background color
APP.setBackGroundColor = function( backcolor ){
		APP.scene.background = new THREE.Color( backcolor );
	}

function rgb2hex ( rgb ) {
	return "#" + rgb.map( function ( value ) {
		return ( "0" + value.toString( 16 ) ).slice( -2 ) ;
	} ).join( "" ) ;
}

// Operation on mouse click
function clickPosition( event ) {
	onDragStart(event);
	// Location of mouse
	var clientX = event.clientX;
	var clientY = event.clientY;


	// Normalization of location
	var mouse = new THREE.Vector2();
	mouse.x = ( ( clientX - APP.renderer.domElement.offsetLeft ) / APP.renderer.domElement.clientWidth ) * 2 - 1;
	mouse.y = - ( ( clientY - APP.renderer.domElement.offsetTop ) / APP.renderer.domElement.clientHeight ) * 2 + 1;

	// Raycasterインスタンス作成
	var raycaster = new THREE.Raycaster();
	// 取得したX、Y座標でrayの位置を更新
	raycaster.setFromCamera( mouse, APP.camera );

	// Indetify crossing objects.
	var intersects = raycaster.intersectObjects( APP.scene.children );
	// Write the most proximal one.
	if (Object.keys(intersects).length > 0) {
		var objid = intersects[0].object.name;
		const target = document.getElementById("ClickedObjectID");
		target.innerHTML = objid;

		if (APP.MarkerOffOn == 1) {
			var x = intersects[ 0 ].point.x;
			var y = intersects[ 0 ].point.y;
			var z = intersects[ 0 ].point.z;

			//Append Jsontable
			var markerName = APP.MarkerPrefix + String(APP.MarkerSuffix);

			APP.addMarker({
				act: 1,
				name: markerName,
				parentid: objid,
				radius: APP.MarkerRadius,
				r: APP.MarkerR,
				g: APP.MarkerG,
				b: APP.MarkerB,
				x: x,
				y: y,
				z: z
			});
		}
	}else{
		const target = document.getElementById("ClickedObjectID");
		target.innerHTML = "Background";
	}
}

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
APP.addMarker = function(markerData, isImportFromFile) {
  var markerData_act = Number(markerData.act);
  var markerData_name = String(markerData.name);
  var markerData_parentid = Number(markerData.parentid);
  var markerData_radius = Number(markerData.radius);
  var markerData_r = Number(markerData.r);
  var markerData_g = Number(markerData.g);
  var markerData_b = Number(markerData.b);
  var markerData_x = Number(markerData.x);
  var markerData_y = Number(markerData.y);
  var markerData_z = Number(markerData.z);

  // CSVファイルからの読み込み時はMarkerがOFFでも描画する(要確認)
  if (APP.MarkerOffOn == 1 || isImportFromFile) {
    var color = rgb2hex([markerData_r, markerData_g, markerData_b]);

    // Add sphere
    var geometry = new THREE.SphereGeometry(1);
    var material = new THREE.MeshBasicMaterial({ color: color });
    var sphere = new THREE.Mesh(geometry, material);

    sphere.scale.set(markerData_radius, markerData_radius, markerData_radius);
    sphere.position.set(markerData_x, markerData_y, markerData_z);
    sphere.name = 'm' + APP.MarkerID.toString();
    APP.scene.add(sphere);

    var NewMarker = {
      act: markerData_act,
      id: APP.MarkerID,
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

    ObjMarkerTable.addData(NewMarker);  // Change database MarkerTable (setData)
    APP.updateMarkerId();
    return true;
  }
  return false;
};

/**
 * MarkerIDを更新する
 */
APP.updateMarkerId = function() {
  APP.MarkerSuffix = APP.MarkerSuffix + 1;
  APP.MarkerID = APP.MarkerID + 1;
  $('#SetSuffixNum').val(APP.MarkerSuffix); // Change suffix for index.html
};

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
APP.renderMarker = function(markerData) {
  var obj = APP.scene.getObjectByName(Number(markerData.parentid));
  if (obj == null) {
    return false;
  }
  return APP.addMarker(markerData, true);
};

// Change the color of the stl object specified by a name after generation.
APP.changeMarkerRadius = function(id, r){
	var name = 'm'+ id.toString();
	var obj = APP.scene.getObjectByName(name);
	console.log(obj);
	if ( obj != undefined ) {
    		obj.scale.set(r,r,r);
		}
	}

// Change the color of the stl object specified by a name after generation.
APP.changeMarkerColor = function(id, objcolor){
	var name = 'm'+ id.toString();
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	}

// Remove a stl object by a name after generation.
APP.removeMarker = function(id){

	// Remove from scene
	var name = 'm'+ id.toString();
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    APP.scene.remove(obj);
	}

        // Remove from json variable
	//var newData = APP.MarkerTable.filter(function(item, index){ if (item.id != id) return true;});
	//APP.MarkerTable = newData
}


var onDragStart = (event) => {
  APP.dragging = true;
	annotate(event);
}

var onDragEnd = (event) => {
	APP.dragging = false;
}

var annotate = (event) => {
  if (!APP.dragging) {
	const { intersect } = getIntersect({
		x: event.offsetX,
		y: event.offsetY,
		camera: APP.camera,
		meshes: APP.getMeshes(),
		container: APP.renderer.domElement,
	})
	updateCursor(intersect && intersect.point);
	return;
  };
  if (!APP.annotation_mode) return;
  const { intersect } = annotateBySphere({
		x: event.offsetX,
		y: event.offsetY,
		camera: APP.camera,
		meshes: APP.getMeshes(),
		container: APP.renderer.domElement,
		radius: APP.AnnotatorRadius || 3,
		ignoreBackFace: null,
  });
  updateCursor(intersect && intersect.point);
  updateMetricsOnAnnotationTable(AnnotationTable)
};
const updateCursor = position => {
	const radius = APP.AnnotatorRadius || 3;
	const cursor = APP.cursor;
	if (position) {
		cursor.position.copy(position);
		const zoom = radius / cursor.geometry.boundingSphere.radius;
		cursor.scale.set(zoom, zoom, zoom);
		cursor.visible = true;
	  } else {
		cursor.visible = false;
	  }
}

const updateMetricsOnAnnotationTable = (annotationTable) => {
	const params = getCurrentParams({ meshes: APP.getMeshes() });
	const areas = params.areas;
	const newRows = annotationTable.getData("active").map(_item => {
		const item = Object.assign({}, _item);
		item.area =  areas[item.id] && areas[item.id].toFixed(0);
		return item;
	})
	annotationTable.updateData(newRows);
};

APP.getMeshes = () => {
	return APP.scene.children.filter(object => object.type === "Mesh" && object.geometry.isBufferGeometry && !object.isCursor);
}


export function StlViewer() {

	// Renderer
	var container = document.getElementById('myCanvas');
	APP.renderer = new THREE.WebGLRenderer( { preserveDrawingBuffer: true } );
	APP.renderer.setSize(window.innerWidth * xratio, window.innerHeight * yratio);
	container.appendChild( APP.renderer.domElement );

	 // Camera
	APP.camera = new THREE.PerspectiveCamera();
	APP.camera.position.z = 400;
	// APP.camera.lookAt(new THREE.Vector3(64, 64, 64));

	// Scene
	APP.scene = new THREE.Scene();
	APP.scene.add( APP.camera );

	// Background Color
	APP.scene.background = new THREE.Color( 0xffffff );
	APP.BackGroundColor == 'White';

	// Light
	APP.directionalLight = new THREE.DirectionalLight(0xffffff);
	APP.directionalLight.position.set(1, 1, 1);
	APP.directionalLight.intensity = 0.8;
	APP.camera.add( APP.directionalLight );
	APP.ambientLight = new THREE.AmbientLight( 0xffffff );
	APP.ambientLight.intensity = 0.5;
	APP.camera.add( APP.ambientLight );

	var min = 0 ;
	var max = 255 ;

	// Controlsを用意
	APP.controls = new THREE.TrackballControls( APP.camera, APP.renderer.domElement );
  APP.controls.rotateSpeed = 10;
  APP.animate();

	// Response to mouse click
		APP.renderer.domElement.addEventListener( 'mousedown', clickPosition, false );
		APP.renderer.domElement.addEventListener('mouseup', onDragEnd, false);
		APP.renderer.domElement.addEventListener('onmousemove', annotate, false);
		APP.renderer.domElement.onmousemove = annotate;
	// Marker Variables
	APP.MarkerOffOn = 0;
	APP.MarkerR = 255;
	APP.MarkerG = 0;
	APP.MarkerB = 0;
	APP.MarkerPrefix = "Marker";
	APP.MarkerSuffix = 0;
	APP.MarkerRadius = 2.0;
	APP.MarkerID     = 1;

	// Cursor 
	var geometry = new THREE.SphereBufferGeometry( 3, 32, 32 );
	var material = new THREE.MeshLambertMaterial( {color: 0xffffff, opacity: 0.3, transparent: true, depthWrite: false} );
	var cursor = new THREE.Mesh( geometry, material );
	cursor.isCursor = true;
	APP.cursor = cursor;
	APP.scene.add( cursor );

	// Boundingbox variables
	var prot = location.protocol;
	var url = prot +"/data/Boundingbox.json";

  // jQuery getJSONを使用
  $.getJSON(url, function(data) {
    APP.BoundingboxX = data.x;
    APP.BoundingboxY = data.y;
    APP.BoundingboxZ = data.z;
  });
}

window.addEventListener( 'resize', onWindowResize, false );
