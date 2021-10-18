//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import * as hdf5 from 'jsfive';
import { MarkerTable } from "./MarkerTable";
import { SurfaceTable } from "./SurfaceTable";

// Change the opacity of all surface objects

APP.addSkeletons = function() {
	APP.scene.traverse(function(obj) {
		if ( (obj instanceof THREE.Mesh === true) && (obj.visible === true) && (obj.name.length === 10) ) {
			var id  = obj.name - 0;
			var col = obj.material.color;
			APP.addSkeletonObject(id, col)
		}
	});
}

APP.removeSkeletons = function() {
	APP.scene.traverse(function(obj) {
		if ( obj.name.match(/line/) ) {
			obj.visible = false;
		}
	});
}


// Add stl objects and a name
APP.generateSkeletons = function() {
	const call_url   = location.protocol+"//"+location.host+"/ws/surface_skeleton";

	const skel_scale       = document.getElementById("SkelScale"); 
	const skel_constant    = document.getElementById("SkelConstant"); 
	const skel_min_voxels  = document.getElementById("SkelMinVoxels"); 
	const skel_max_paths   = document.getElementById("SkelMaxPaths"); 
	const skel_smoothness  = document.getElementById("SkelSmoothness"); 
	const skel_extra_after = document.getElementsByName("SkelExtraAfter"); 

	var request = {};
	request["mode"]      = "skeleton";
	request["scale"]     = String(skel_scale.value);
	request["constant"]  = String(skel_constant.value);
	request["min_voxel"] = String(skel_min_voxels.value);
	request["max_path"]  = String(skel_max_paths.value);
	request["smooth"]    = String(skel_smoothness.value);
	request["extra_after"] = String(skel_extra_after.value) === 'true';
	request["element"]   = [];
	// Get JSON variable that shows the skeletons "ids and colors", and associated markers.
	var rows = SurfaceTable.searchRows("act", "=",  true);
	for (var i in rows) {
		var id  = rows[i].getData().id;
  		var r   = rows[i].getData().r;
  		var g   = rows[i].getData().g;
  		var b   = rows[i].getData().b;
  		var col = r*256*256+g*256+b*1;
		//console.log('Target id: ', id);
		var element = {}
		element.id = id
		element.color = col
		// Remove current skeleton
		var name = 'line' + ( '0000000000' + id ).slice( -10 );
		var obj = APP.scene.getObjectByName(name);
		if ( obj != undefined ) {
			//obj.geometry.dispose();
			//obj.material.dispose();
    		APP.scene.remove(obj);
    		APP.disposeNode(obj);
		}
		// Get marker points
  		var rows_marker = MarkerTable.searchRows("parentid", "=",  id);
  		var markerlocs = [];
		for (var j in rows_marker) {
				var id_marker  = rows_marker[j].getData().id;
				var mx = rows_marker[j].getData().x;
				var my = rows_marker[j].getData().y;
				var mz = rows_marker[j].getData().z;
				//console.log('Marker id: ', id_marker);
				//console.log('x,y,z: ',mx,my,mz);
				markerlocs.push([mx, my, mz])
				}
		element.markerlocs = markerlocs
		console.log('element: ', element)
		request["element"].push(element)
		}
	// console.log(request)


	//Send request to Server
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
				alert("No skeleton.");
				return false;
				}
	    }
	}
	req.open( 'POST', call_url , false);
	req.setRequestHeader( 'Content-Type', 'application/json' );
	req.send(JSON.stringify(request));

	for (const elem of request["element"]) {
		console.log("Element: ", elem)
		APP.addSkeletonObject(elem.id, elem.color)
		}

	}
//


// Add stl objects and a name
APP.addSkeletonObject = function(id, col) {

	if (APP.SkeletonMode == 0){
		return false;
		}

	const call_url   = location.protocol+"//"+location.host+"/ws/surface_skeleton";
	const target_url = location.protocol+"//"+location.host+"/skeleton/whole/" + ( '0000000000' + id ).slice( -10 ) + ".hdf5";
	const filename   = ( '0000000000' + id ).slice( -10 ) + ".hdf5";
	const name       = 'line' + ( '0000000000' + id ).slice( -10 );
	
	// Revive if it already exists.
	// console.log('Name: ', name)
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		// console.log('Obj: ', obj)
		obj.visible = true;
		return true;
		}

	// Request the surface mesh generation to the server if it does not exist.
	var xhr = new XMLHttpRequest();
	xhr.open("HEAD", target_url, false);  //同期モード promise method
	xhr.send(null);
	if(xhr.status == 404) {
				// alert("No skeleton.");
				console.log('No skeleton data:', id);
				return false;
		}

	//
	fetch(target_url)
	  .then(function(response) {
	    return response.arrayBuffer() 
	  })
	  .then(function(buffer) {
	    //
	    //
	    var f = new hdf5.File(buffer, filename);
	    let g1 = f.get('vertices');
	    let g2 = f.get('edges');
	    var data_vertices = g1.value;
	    var data_edges    = g2.value;
	    
	    data_vertices = splitArray(data_vertices, 3);
	    data_edges    = splitArray(data_edges, 2);
	    
	    
		var i1 = undefined;
		var i2 = undefined;
		var v1 = undefined;
		var v2 = undefined;
		// console.log(data_vertices)
		// console.log('Length vertices: ' + data_vertices.length);
		// console.log('Length edges   : ' + data_edges.length);
		
		////// Uncaught TypeError: Cannot read property '0' of undefined
		
		if (typeof data_vertices !== "object"){
 			console.log('Not skeleton data.');
			return false;
		}
		if(typeof(data_vertices[0])==="undefined"){
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
			color: col,  //0x000000
			linewidth: 3,
			fog:true
		});
		
		for(let i=0;i< data_edges.length;i++){
			i1 = data_edges[i][0];
			i2 = data_edges[i][1];

//			console.log('Vertices ID: ', i1, i2 );
//			console.log('data_vertices[i1]: ', data_vertices[i1] );
//			console.log('data_vertices[i2]: ', data_vertices[i2] );

			v1 = new THREE.Vector3( data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
			v2 = new THREE.Vector3( data_vertices[i2][0], data_vertices[i2][1], data_vertices[i2][2]);
			geometry.vertices.push(v1, v2);
			}
		var line = new THREE.LineSegments( geometry, material );   
		
		
		line.name = name;
		// console.log(line.name);
		APP.scene.add( line );	    
	    //
	    //
	    //
	  });
	}


// Change the color of a skeleton object specified by a name.
APP.changeSkeletonObjectColor = function(id, col) {
	name = 'line' + ( '0000000000' + id ).slice( -10 );
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		obj.material.color.setHex( col );
		}
	}


// Remove a stl object by the name.
APP.removeSkeletonObject = function(id) {
	name = 'line' + ( '0000000000' + id ).slice( -10 );
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		// APP.scene.remove(obj);
		obj.visible = false;
		}
	}


function splitArray(array, part) {
    var tmp = [];
    for(var i = 0; i < array.length; i += part) {
        tmp.push(array.slice(i, i + part));
    }
    return tmp;
}





