//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import { updateColorOptionsOnAnnotator } from "./PaintTable";
import { paintManager } from "./SyncPaint";
import { SurfaceTable } from "./SurfaceTable";

export const getSurfaceName = id => {
	return ( '0000000000' + id ).slice( -10 );
}

// Add surface objects and a name
APP.addSurfaceObject = function(id, col) {

	if (APP.SphereMode == 1){
		return false;
		}

	const name =  getSurfaceName(id);
	const call_url   = location.protocol+"//"+location.host+"/ws/surface_skeleton";
	const target_url = location.protocol+"//"+location.host+"/surface/whole/" + name + ".stl";

	// Revive it if already exists.
	// console.log('Name: ', name)
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		// console.log('Obj: ', obj)
		obj.visible = true;
		obj.material.opacity = APP.surface_opacity;
		paintManager.addSurface(name);
		return true;
		}

	// Request the surface mesh generation to the server if it does not exist.
	var xhr = new XMLHttpRequest();
	xhr.open("HEAD", target_url, false);  //同期モード promise method
	xhr.send(null);
	if(xhr.status == 404) {

		// Obtain smoothing option
		const SmoothMeth = document.getElementsByName("SmoothingMethod"); // document.SmoothingMethod;
		const NumIter = document.getElementById("SmoothingNumIters"); // SmoothingNumIters;
		let Smeth = "";
		for (let i = 0; i < SmoothMeth.length; i++){
			if(SmoothMeth[i].checked){ //(SmoothMeth[i].checked === true)と同じ
				Smeth = SmoothMeth[i].value;
				break;
			}
		}

		//Send request
		var data = { mode: "surface", id: id, smooth_method: Smeth, num_iter: String(NumIter.value) }; // POSTメソッドで送信するデータ
		var req = new XMLHttpRequest();
		req.onreadystatechange = function()
		{
		    var READYSTATE_COMPLETED = 4;
		    var HTTP_STATUS_OK = 200;

		    if( this.readyState == READYSTATE_COMPLETED
		     && this.status == HTTP_STATUS_OK )
		    {
		        // レスポンスの表示
		        if (this.responseText == "False") {
					alert("No surface.");
					return false;
					}
		    }
		}
		req.open( 'POST', call_url , false);
		// サーバに対して解析方法を指定する
		req.setRequestHeader( 'Content-Type', 'application/json' );
		// データをリクエスト ボディに含めて送信する
		req.send(JSON.stringify(data));
//

//			以前、GET methodで
//			var req = new XMLHttpRequest();
//			req.open("get", call_url+id, false);
//			req.send(null);
//			if (req.responseText == "False") {
//				alert("No surface.");
//				return false;
//				}
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

	var rows = SurfaceTable.searchRows("act", "=",  true);
	for (var i in rows) {
		var id  = rows[i].getData().id;
  		var r   = rows[i].getData().r;
  		var g   = rows[i].getData().g;
  		var b   = rows[i].getData().b;
		if (invisible == 1) {
			APP.removeSurfaceObject(id);
			APP.removeSkeletonObject(id);
		} else {
			var col = r*256*256+g*256+b*1 ;
			APP.addSurfaceObject(id, col);
			APP.addSkeletonObject(id, col);
		}
	}
}
// if (obj instanceof THREE.Mesh === true && /^\d*$/.test(obj.name) && obj.name.length === 10 ) {


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



