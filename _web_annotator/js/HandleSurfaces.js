//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import { updateColorOptionsOnAnnotator } from "./PaintTable";
import { paintManager } from "./SyncPaint";

export const getSurfaceName = id => {
	return ( '0000000000' + id ).slice( -10 );
}

// Add surface objects and a name
APP.addSurfaceObject = function(id, col) {

	const name =  getSurfaceName(id);
	const call_url   = location.protocol+"//"+location.host+"/ws/surface?id=";
	const target_url = location.protocol+"//"+location.host+"/surface/whole/" + name + ".stl";

	// Revive it if already exists.
	// console.log('Name: ', name)
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		// console.log('Obj: ', obj)
		obj.visible = true;
		paintManager.addSurface(name);
		return true;
		}

	// Request the surface mesh generation to the server if it does not exist.
	var xhr = new XMLHttpRequest();
	xhr.open("HEAD", target_url, false);  //同期モード
	xhr.send(null);
	if(xhr.status == 404) {
			var req = new XMLHttpRequest();
			req.open("get", call_url+id, false);
			req.send(null);
			if (req.responseText == "False") {
				alert("No surface.");
				return false;
				}
	}
	// console.log('Mesh prepared.');

	// Load the stl file then generate mesh object.
	var loader = new THREE.STLLoader();
	loader.load(target_url, function(bufferGeometry) {
	  if (bufferGeometry.isBufferGeometry) {
		  bufferGeometry.attributes.color = bufferGeometry.attributes.color || bufferGeometry.attributes.position.clone();
		  bufferGeometry.attributes.color.array.fill(1);
		  bufferGeometry.attributes.color.needsUpdate = true;
		  bufferGeometry.colorsNeedUpdate = true;
	  }
	  // console.log('Stl loaded.');
	  const meshMaterial = new THREE.MeshPhongMaterial({
		  color: col,
		  specular: 0x776666,
		  shininess: 0.2,
		  vertexColors: THREE.FaceColors,
		  transparent: true,
		  opacity: APP.surface_opacity,
		  side: THREE.DoubleSide
	  }) // APP.surface_opacity
	  var mesh = new THREE.Mesh(bufferGeometry, meshMaterial);
      mesh.name = name;
      mesh.scale.set(1, 1, 1);
      // mesh.material.side = THREE.DoubleSide;
      APP.scene.add(mesh);

	  // console.log(mesh.name);

	  updateColorOptionsOnAnnotator();
	  paintManager.addSurface(name);
	});
}

// Change the opacity of all surface objects

APP.changeSurfaceObjectOpacity = function(opacity) {
	// console.log('Input opacity: ', opacity)
	var invisible = 0;
	if ( opacity == -2 ){
		invisible = 1;
	} else if ( opacity == -1 ){
		APP.surface_opacity = 1;
	} else if (opacity == 0) {
		APP.surface_opacity = APP.surface_opacity_reserved;
	} else {
		APP.surface_opacity = opacity;
		APP.surface_opacity_reserved = opacity;
	};

	APP.scene.traverse(function(obj) {
		if (obj instanceof THREE.Mesh === true && /^\d*$/.test(obj.name) && obj.name.length === 10 ) {
			if (invisible == 1) {
				obj.visible = false;
				} else {
				obj.visible = true;
				obj.material.opacity = APP.surface_opacity;
				}
			}
		});
}


// Change the color of a surface object specified by the name.
APP.changeSurfaceObjectColor = function(id, objcolor) {
	const name =  getSurfaceName(id);
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	}


// Remove a stl object by a name after generation.
APP.removeSurfaceObject = function(id) {
	const name =  getSurfaceName(id);
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		// APP.scene.remove(obj);
		obj.visible = false;
		}
		paintManager.removeSurface(name);
	}



