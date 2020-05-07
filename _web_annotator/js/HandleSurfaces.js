//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import { updateColorOptionsOnAnnotator } from "./AnnotationTable";

// Add surface objects and a name
APP.addSurfaceObject = function(id, objcolor) {
	const call_url   = location.protocol+"//"+location.host+"/ws/surface?id=";
	const target_url = location.protocol+"//"+location.host+"/surface/whole/" + ( '0000000000' + id ).slice( -10 ) + ".stl";

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
	// console.log('Mesh prepared:');

	var loader = new THREE.STLLoader();
	loader.load(target_url, function(bufferGeometry) {
	  if (bufferGeometry.isBufferGeometry) {
		  bufferGeometry.attributes.color = bufferGeometry.attributes.color || bufferGeometry.attributes.position.clone();
		  bufferGeometry.attributes.color.array.fill(1);
		  bufferGeometry.attributes.color.needsUpdate = true;
		  bufferGeometry.colorsNeedUpdate = true;
	  }
	  console.log('Stl loaded:');
	  const meshMaterial = new THREE.MeshPhongMaterial({
		  color: objcolor,
		  specular: 0x776666,
		  shininess: 0.2,
		  vertexColors: THREE.FaceColors,
		  side: true
	  }) // 	    	  opacity: 0.4,
	  var mesh = new THREE.Mesh(bufferGeometry, meshMaterial);
      mesh.name = id;
      mesh.scale.set(1, 1, 1);
      mesh.material.side = THREE.DoubleSide;
      APP.scene.add(mesh);

	  updateColorOptionsOnAnnotator();
	});
}

// Change the color of the stl object specified by a name after generation.
APP.changeSurfaceObjectColor = function(name, objcolor) {
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	
	name_centerline = 'line' + name.toString();
	console.log(name_centerline);
	var obj = APP.scene.getObjectByName(name_centerline);
	if ( obj != undefined ) {
    		obj.material.color.setHex( objcolor );
		}
	}

// Remove a stl object by a name after generation.
APP.removeSurfaceObject = function(id) {
	var obj = APP.scene.getObjectByName(id);
	if ( obj != undefined ) {
    	    APP.scene.remove(obj);
	}
	/*
	name_centerline = 'line' + name.toString();
	console.log(name_centerline);
	var obj = APP.scene.getObjectByName(name_centerline);
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
	}
	*/
	}



