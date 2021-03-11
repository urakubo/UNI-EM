//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import * as hdf5 from 'jsfive';
import { SurfaceTable } from "./SurfaceTable";

// Change the opacity of all surface objects

APP.addSpheres = function() {
	
	var rows = SurfaceTable.searchRows("act", "=",  true);
	for (var i in rows) {
		var id  = rows[i].getData().id;
  		var r   = rows[i].getData().r;
  		var g   = rows[i].getData().g;
  		var b   = rows[i].getData().b;
  		var col = r*256*256+g*256+b*1;
  		APP.addSphereObject(id, col);
  	}

}

APP.removeSpheres = function() {
	APP.scene.traverse(function(obj) {
		if ( obj.name.match(/Spheres/) ) {
			obj.visible = false;
		}
	});
}


// Add stl objects and a name
APP.addSphereObject = function(id, col) {

	if (APP.SphereMode == 0){
		return false;
		}

	const target_url = location.protocol+"//"+location.host+"/skeleton/whole/" + ( '0000000000' + id ).slice( -10 ) + ".hdf5";
	const filename   = ( '0000000000' + id ).slice( -10 ) + ".hdf5";
	const name       = 'Spheres' + ( '0000000000' + id ).slice( -10 );
	
	// Revive if it already exists.
	// console.log('Name: ', name)
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		// console.log('Obj: ', obj)
		obj.visible = true;
		return true;
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
	    let g3 = f.get('radiuses');
	    var data_vertices = g1.value;
	    var data_edges    = g2.value;
	    var data_radiuses = g3.value;
	    
	    data_vertices = splitArray(data_vertices, 3);
	    data_edges    = splitArray(data_edges, 2);
	    data_radiuses = splitArray(data_radiuses, 1);
	    
	    
		var i1 = undefined;
		var i2 = undefined;
		var v1 = undefined;
		var v2 = undefined;
		// console.log(data_vertices)
		// console.log('Length vertices: ' + data_vertices.length);
		// console.log('Length edges   : ' + data_edges.length);
		if (isNaN(data_vertices[0][0]) == true) {
			// console.log(data_vertices);
			console.log('No morphological data.');
			return false;
		}

		var geometry = new THREE.Geometry();
		var material = new THREE.LineBasicMaterial({
			color: col,  //0x000000
			linewidth: 3,
			fog:true
		});
		
		
		var spheres = new THREE.Group();
		for(var i=0;i< data_edges.length;i++){
			i1 = data_edges[i][0];
			i2 = data_edges[i][1];

			// console.log('Vertices ID: ', i1, i2 );

			v1 = new THREE.Vector3( data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
			v2 = new THREE.Vector3( data_vertices[i2][0], data_vertices[i2][1], data_vertices[i2][2]);
			geometry.vertices.push(v1, v2);


			// Create sphere object
			var radius = data_radiuses[i1];
			if ( (i1 % 20 == 1) || (radius < 0.1) ) {
				// if ( data_vertices[i1][2] <= APP.BoundingboxZ * 0.05 ) {continue;}
				// if ( data_vertices[i1][1] <= APP.BoundingboxY * 0.05 ) {continue;}
				// if ( data_vertices[i1][0] <= APP.BoundingboxX * 0.05 ) {continue;}
				// if ( data_vertices[i1][2] >= APP.BoundingboxZ * 0.95 ) {continue;}
				// if ( data_vertices[i1][1] >= APP.BoundingboxY * 0.95 ) {continue;}
				// if ( data_vertices[i1][0] >= APP.BoundingboxX * 0.95 ) {continue;}
				// console.log(data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
			
				const geometry  = new THREE.SphereGeometry( radius,  32, 32);
				const material  = new THREE.MeshLambertMaterial( {color: col, opacity: 0.5, transparent: true, depthWrite: false} );
				const vertice_r = new THREE.Mesh( geometry, material );
				vertice_r.position.set(data_vertices[i1][0], data_vertices[i1][1], data_vertices[i1][2]);
				spheres.add( vertice_r )

				}
			}
		var line = new THREE.LineSegments( geometry, material );
		spheres.add( line )

		spheres.name = name;
		APP.scene.add( spheres );
	    //
	    //
	  });
	}


// Change the color of a skeleton object specified by a name.
APP.changeSphereObjectColor = function(id, col) {
	name = 'Spheres' + ( '0000000000' + id ).slice( -10 );
	var obj = APP.scene.getObjectByName(name);
	if ( obj != undefined ) {
		obj.material.color.setHex( col );
		}
	}


// Remove a stl object by the name.
APP.removeSphereObject = function(id) {
	name = 'Spheres' + ( '0000000000' + id ).slice( -10 );
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





