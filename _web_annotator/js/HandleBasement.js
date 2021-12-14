import { APP } from "./APP";
import { PaintTable } from "./PaintTable";
import _ from "lodash";
import { paintManager } from "./SyncPaint";
import { SurfaceTable } from "./SurfaceTable";
import { getSurfaceName } from "./HandleSurfaces";
import * as zlib from "zlib";
import {
	getIntersect,
	annotateBySphere,
	getCurrentParams,
	getChanges,
	setAnnotation,
	getPaintID
} from "./three_annotator/index";

var xratio = 0.6;
var yratio = 0.95;
var frustumSize = 1000;

function animate() {
	APP.renderer.render( APP.scene, APP.camera );
	APP.controls.update();
	requestAnimationFrame( animate );
};


APP.dragging = false;
APP.paint_mode = false;
APP.paint_on = true;
APP.paint_overwriteB = false;


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
	var ids = [];
	var intersected_surfaces = [];
	var intersected_objects = [];
	for (let i = 0; i < intersects.length; i++) {
		var name = intersects[i].object.name;
		if (/^\d*$/.test(name) && name.length === 10) { // /^\d*$/ 符号や小数点を許容しない数値
				intersected_surfaces.push(intersects[i]);
////
			  	ids = getPaintID({
					x: event.offsetX,
					y: event.offsetY,
					camera: APP.camera,
					meshes: APP.getMeshes(),
					container: APP.renderer.domElement,
			  		});
////
				//console.log('ids: ', ids);
			}
		intersected_objects.push(intersects[i]);
	}

	if (APP.MarkerMode == 1 && intersected_surfaces.length > 0) {
		// If in the marker mode, put a marker  (this should be moved to HandleMarker.js).
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

	const target = document.getElementById("ClickedObjectID");
	if (intersected_objects.length <= 0) {
		target.innerHTML = "Background";
	}else if (typeof ids[0] === "undefined") {
		target.innerHTML = intersected_objects[ 0 ].object.name;
	}else{
		target.innerHTML = intersected_objects[ 0 ].object.name +"-"+ids[0];
	} // endif
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
  if (!APP.paint_mode) return;
  const { intersect } = annotateBySphere({
		x: event.offsetX,
		y: event.offsetY,
		camera: APP.camera,
		meshes: APP.getMeshes(),
		container: APP.renderer.domElement,
		radius: getCursorRadius(APP.AnnotatorRadius),
		ignoreBackFace: null,
  });
  updateCursor(intersect && intersect.point);
  updateMetricsOnPaintTable()
  syncAnnotation();
};


const compress = paintData => paintData && zlib.gzipSync(Buffer.from(paintData)).buffer;
const decompress = compressedData => compressedData && new Uint8Array(zlib.gunzipSync(Buffer.from(compressedData)).buffer);

const syncAnnotation = _.debounce(() => {
	const changes = getChanges({meshes: APP.getMeshes()});
	if(Object.keys(changes).length > 0) {
		for(const objectChanges of Object.values(changes)) {
			for(const colorChanges of Object.values(objectChanges)) {
				colorChanges.painted = compress(colorChanges.painted);
			}
		}
		paintManager.update({changes})
	}
}, 1000, { maxWait: 1000 });

paintManager.emitter.on("update", data => {
	if(data.room_id !== "list") {
		console.log(data.room_id);
		const [surfaceId, colorId] = data.room_id.split("-");
		const mesh = APP.getMeshes().find(mesh => mesh.name === surfaceId);
		if(!mesh) {
			console.error("mesh not found")
			return;
		}
		setAnnotation({ mesh, colorId, data: {
			...data,
			painted: decompress(data.painted),
		}})
		updateMetricsOnPaintTable();
	}
})

const getCursorRadius = annotatorRadius => (annotatorRadius || 0.3);

const updateCursor = position => {
	if (APP.cursor.visible === false) {
		return;
	}
	const radius = getCursorRadius(APP.AnnotatorRadius);
	const cursor = APP.cursor;
	if (position) {
		cursor.position.copy(position);
		const zoom = radius;
		cursor.scale.set(zoom, zoom, zoom);
		cursor.material.opacity = 0.3;
	} else {
		cursor.material.opacity = 0;
	}
}

export const updateMetricsOnPaintTable = () => {
	const activeSurfaces = new Set(SurfaceTable.getData()
		.filter(row => row.act)
		.map(row => getSurfaceName(row.id))
	);
	const meshes = APP.getMeshes().filter(mesh => activeSurfaces.has(mesh.name));
	const params = getCurrentParams({ meshes });
	const areas = params.areas;
	const newRows = PaintTable.getData("active").map((item = {}) => {
		return {
			...item,
			area: areas[item.id]
		}
	})
	PaintTable.updateData(newRows);
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
	APP.directionalLight.position.set(0, 10, 0);  //default; light shining from top
	APP.directionalLight.target.position.set(0, 0, 0);  //default; light shining from top
	APP.directionalLight.intensity = 0.8;
	//APP.camera.add( APP.directionalLight );
	APP.scene.add( APP.directionalLight );

	
	APP.ambientLight = new THREE.AmbientLight( 0xffffff );
	APP.ambientLight.intensity = 0.5;
	APP.camera.add( APP.ambientLight );

	// var min = 0 ;
	// var max = 255 ;

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
	var geometry = new THREE.SphereBufferGeometry( 1, 32, 32 );
	var material = new THREE.MeshLambertMaterial( {color: 0xffffff, opacity: 0, transparent: true, depthWrite: false} );
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

	// Sphere
	APP.SphereMode   = 0;

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
		APP.directionalLight.target.position.set(APP.BoundingboxX/2.0, APP.BoundingboxY/2.0, APP.BoundingboxZ/2.0); 
		window.DirLightX(false)
		window.DirLightY(false)
		window.DirLightZ(false)
		
		// https://threejsfundamentals.org/threejs/lessons/threejs-lights.html
    });
}
