//
//
//
//
//
import { APP } from "./APP";
import { parseCSV, csvFormatter } from "./csv";
import { MarkerTable } from "./MarkerTable";

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
  if (APP.MarkerMode == 1 || isImportFromFile) {
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
    MarkerTable.addData(NewMarker);  // Change database MarkerTable (setData)
    updateMarkerId();
    return true;
  }
  return false;
};


function rgb2hex ( rgb ) {
	return "#" + rgb.map( function ( value ) {
		return ( "0" + value.toString( 16 ) ).slice( -2 ) ;
	} ).join( "" ) ;
}

/**
 * MarkerIDを更新する
 */
function updateMarkerId() {
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
}


