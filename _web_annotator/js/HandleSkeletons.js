//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";


// Add stl objects and a name
APP.addSkeletonObject = function(id, objcolor) {
		var data_vertices = obtainDATA('vertices', id);
		var data_edges    = obtainDATA('edges', id);
		
		var i1 = undefined;
		var i2 = undefined;
		var v1 = undefined;
		var v2 = undefined;
		
		console.log('Length vertices: ' + data_vertices.length);
		if (isNaN(data_vertices[0][0]) == true) {
			console.log(data_vertices);
			console.log('No morphological data.');
			return false;
		}
		// console.log('Color: ' + objcolor);
		var geometry = new THREE.Geometry();
		var material = new THREE.LineBasicMaterial({
			color: objcolor,  //0x000000
			linewidth: 3,
			fog:true
		});
		for(var i=0;i< data_edges.length;i++){
			i1 = data_edges[i][0];
			i2 = data_edges[i][1];
			//console.log(data_edges)

			v1 = new THREE.Vector3( data_vertices[i1][0],data_vertices[i1][1],data_vertices[i1][2]);
			v2 = new THREE.Vector3( data_vertices[i2][0],data_vertices[i2][1],data_vertices[i2][2]);
			geometry.vertices.push(v1, v2);
			//console.log(data_vertices[i1][0]+xshift,data_vertices[i1][1]+yshift,data_vertices[i1][2]+zshift)
			}
		var line = new THREE.LineSegments( geometry, material );

		line.name = 'line' + id.toString();
		console.log(line.name);
		APP.scene.add( line );
		//renderer.render(scene, camera);
	}



function obtainDATA(name, id){
		var req = new XMLHttpRequest();
		var response = undefined;  // 値を引き取るための変数
		req.onload = function(){
		response = req.response;  // 親ブロック（xhrStart）のresponse変数に引き継ぐ
			}
		req.open("get", "./ws/skeleton?variable="+name+"&id="+id, false);
		req.send(null);
		return convertCSVtoArray(response);
	}


function convertCSVtoArray(responseText){
		//改行ごとに配列化
		var arr = responseText.split('\n');
		// console.log('Length: ' + arr.length); 

		//1次元配列を2次元配列に変換
		var res = [];
		for(var i = 0; i < arr.length; i++){
			//空白行が出てきた時点で終了
			if(arr[i] == '') break;
			//","ごとに配列化
			res[i] = arr[i].split(',');

			for(var i2 = 0; i2 < res[i].length; i2++){
				//数字の場合は「"」を削除
				if(res[i][i2].match(/\-?\d+(.\d+)?(e[\+\-]d+)?/)){
					res[i][i2] = parseFloat(res[i][i2].replace('"', ''));
				}
			}
		}
		return res;
	}


