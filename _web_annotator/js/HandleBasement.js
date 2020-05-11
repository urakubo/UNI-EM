import { APP } from "./APP";
import { AnnotationTable } from "./AnnotationTable";

var xratio = 0.6;
var yratio = 0.95;
var frustumSize = 1000;

function animate() {
	APP.renderer.render( APP.scene, APP.camera );
	APP.controls.update();
	requestAnimationFrame( animate );
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


// Draw bounding box
APP.addBoundingBox = function(){

	if ( APP.BackGroundColor == 'Black'){
		  var mat = new THREE.LineBasicMaterial( { color: 0xFFFFFF, linewidth: 2 } );
		  }
	else{
		var mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
		}

	var geometry = new THREE.BoxBufferGeometry( APP.BoundingboxX, APP.BoundingboxY, APP.BoundingboxZ );
	var geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )

	var boundingbox = new THREE.LineSegments( geo, mat );
	boundingbox.name = 'BoundingBox';
	boundingbox.scale.set(1,1,1);
	APP.scene.add(boundingbox);
	APP.BoundingBox = 'On';
	boundingbox.translateX( APP.BoundingboxX / 2 );
	boundingbox.translateY( APP.BoundingboxY / 2 );
	boundingbox.translateZ( APP.BoundingboxZ / 2 );
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
	
	// Obtain crossing surface objects.
	var intersected_surfaces = [];
	for (let i = 0; i < intersects.length; i++) {
		var name = intersects[i].object.name;
		if (/^\d*$/.test(name) && name.length === 10) {
				intersected_surfaces.push(intersects[i]);
			}
		}
	
	/*
	intersects.traverse(function(obj) {
		if (/^\d*$/.test(obj.object.name) && obj.object.name.length === 10 ) {
			intersected_surfaces.push(intersects[i]);
			}
		})
	*/

	// Put a marker if in the marker mode (this should be moved to HandleMarker.js).
	// Show the ID if not.
	if (intersected_surfaces.length > 0) {
		// Get the most proximal one
		var name = intersected_surfaces[ 0 ].object.name;
		const target = document.getElementById("ClickedObjectID");
		target.innerHTML = name;

		if (APP.MarkerMode == 1) {
			var x = intersected_surfaces[ 0 ].point.x;
			var y = intersected_surfaces[ 0 ].point.y;
			var z = intersected_surfaces[ 0 ].point.z;

			//Append Jsontable
			var markerName = APP.MarkerPrefix + String(APP.MarkerSuffix);

			APP.addMarker({
				act: 1,
				name: markerName,
				parentid: name,
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
	if (APP.cursor.visible === false) {
		return;
	}
	const radius = APP.AnnotatorRadius || 3;
	const cursor = APP.cursor;
	if (position) {
		cursor.position.copy(position);
		const zoom = radius / cursor.geometry.boundingSphere.radius;
		cursor.scale.set(zoom, zoom, zoom);
		cursor.opacity = 0.3;
	  } else {
		cursor.opacity = 0;
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


export function launchAnnotator() {

	// Renderer
	var container = document.getElementById('myCanvas');
	APP.renderer = new THREE.WebGLRenderer( { preserveDrawingBuffer: true } );
	APP.renderer.setSize(window.innerWidth * xratio, window.innerHeight * yratio);
	container.appendChild( APP.renderer.domElement );

	// Initilize camera
	APP.camera = new THREE.PerspectiveCamera();

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
    APP.controls.staticMoving = false;
	APP.controls.dynamicDampingFactor = 1.0; // staticMoving = false のときの減衰量
	animate();

	// Response to mouse click
	APP.renderer.domElement.addEventListener( 'mousedown', clickPosition, false );
	APP.renderer.domElement.addEventListener('mouseup', onDragEnd, false);
	APP.renderer.domElement.addEventListener('onmousemove', annotate, false);
	APP.renderer.domElement.onmousemove = annotate;

	// Paint
	// Cursor
	var geometry = new THREE.SphereBufferGeometry( 3, 32, 32 );
	var material = new THREE.MeshLambertMaterial( {color: 0xffffff, opacity: 0.3, transparent: true, depthWrite: false} );
	var cursor = new THREE.Mesh( geometry, material );
	cursor.isCursor = true;
	cursor.name = 'cursor';
	APP.cursor = cursor;
	APP.cursor.visible = false;
	APP.scene.add( cursor );

    // Marker
	APP.MarkerMode = 0;
	APP.MarkerR = 255;
	APP.MarkerG = 0;
	APP.MarkerB = 0;
	APP.MarkerPrefix = "Marker";
	APP.MarkerSuffix = 0;
	APP.MarkerRadius = 0.1;
	APP.MarkerID     = 1;

	// Surface opacity
	APP.surface_opacity          = 1.0;
	APP.surface_opacity_reserved = 0.5;

	// Skeleton
	APP.SkeletonMode = 0;

	//Boundingbox
	const call_url   = location.protocol+"//"+location.host+"/surface/VolumeDescription.json";
	$.getJSON(call_url).done(function(data) {
		//data_parsed = JSON.parse(data);
		console.log(data)
        APP.BoundingboxX = data.boundingbox_um.x;
		APP.BoundingboxY = data.boundingbox_um.y;
		APP.BoundingboxZ = data.boundingbox_um.z;
		APP.BoundingboxMax = Math.max(APP.BoundingboxX, APP.BoundingboxY, APP.BoundingboxZ);
		console.log('APP.BoundingboxMax: ', APP.BoundingboxMax)
		window.CenterXY()
    });
}


window.addEventListener( 'resize', onWindowResize, false );


