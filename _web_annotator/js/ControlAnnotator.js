import { APP } from "./APP";

//
var xratio = 0.6;
var yratio = 0.95;
//

// Executed when the window size is changed.
window.addEventListener('resize', function() {
	// サイズを取得
	const width = window.innerWidth;
	const height = window.innerHeight;

	// カメラのアスペクト比を正す
	APP.camera.aspect = (width * xratio) / (height * yratio);
	APP.camera.updateProjectionMatrix();

	// レンダラーのサイズを調整する
	APP.renderer.setPixelRatio(window.devicePixelRatio);
	APP.renderer.setSize(width * xratio, height * yratio);
	}, false );

// Mode
window.ChangeMode = function (mode) {
	switch (mode) {
		case "view":
//			console.log("view")
			APP.MarkerMode   = 0;
			APP.SkeletonMode = 0;
			APP.SphereMode   = 0;
			APP.cursor.visible = false;
			switchAnnotation(0);
			APP.changeSurfaceObjectOpacity(-1);
			APP.removeSkeletons();
			APP.removeSpheres();
			break;
		case "point":
//			console.log("point")
			APP.MarkerMode   = 1;
			APP.SkeletonMode = 0;
			APP.SphereMode   = 0;
			APP.cursor.visible = false;
			switchAnnotation(0);
			APP.changeSurfaceObjectOpacity(-1);
			APP.removeSkeletons();
			APP.removeSpheres();
			break;
		case "paint":
//			console.log("paint")
			APP.MarkerMode   = 0;
			APP.SkeletonMode = 0;
			APP.SphereMode   = 0;
			APP.cursor.visible = true;
			switchAnnotation(1);
			APP.changeSurfaceObjectOpacity(-1);
			APP.removeSkeletons();
			APP.removeSpheres();
			break;
		case "skeleton":
//			console.log("skeleton")
			APP.MarkerMode   = 0;
			APP.SkeletonMode = 1;
			APP.SphereMode   = 0;
			APP.cursor.visible = false;
			switchAnnotation(0);
			APP.changeSurfaceObjectOpacity(0);
			APP.addSkeletons();
			APP.removeSpheres();
			break;
		case "sphere":
//			console.log("shpere")
			APP.MarkerMode   = 0;
			APP.SkeletonMode = 0;
			APP.SphereMode   = 1;
			APP.cursor.visible = false;
			switchAnnotation(0);
			APP.changeSurfaceObjectOpacity(-2);
			APP.removeSkeletons();
			APP.addSpheres();
			break;		
		default:
    		console.log(`Error. Mode ${mode} cannot be interpreted.`);
		}
	}
//
// app/index.jsで使っている
//
window.MarkerOffOn = function (ischecked) {
		if( ischecked == true ) {
      		APP.MarkerOffOn = 1;
   			}
		else {
			APP.MarkerOffOn = 0;
			}
      }


window.SaveImage = function (ischecked) {
	let canvas = document.getElementById("myCanvas").querySelector('canvas');

	let link = document.createElement("a");
	link.href = canvas.toDataURL("image/png");
	link.download = "Screenshot.png";
	link.click();
	}


//
// View
//
window.BackgroundWhiteBlack = function (ischecked) {
		if( ischecked == true ) {
			APP.scene.background = new THREE.Color( 0x000000 );
			APP.BackGroundColor = 'Black';
			setBoundingBoxColor( 0xffffff );
   			}
		else {
			APP.scene.background = new THREE.Color( 0xffffff );
      		APP.BackGroundColor = 'White';
      		setBoundingBoxColor( 0x000000 );
			}
      }
window.DirLight = function (isnum) {
		APP.directionalLight.intensity = isnum / 100;
      }

window.AmbLight = function (isnum) {
		APP.ambientLight.intensity = isnum / 100;
      }

window.CenterXY = function () {
	APP.camera.up.set(0,1,0);
	APP.camera.position.set( APP.BoundingboxX/2.0, APP.BoundingboxY/2.0, APP.BoundingboxMax*3.0);
	APP.camera.lookAt(APP.BoundingboxZ/2.0, APP.BoundingboxY/2.0, APP.BoundingboxX/2.0);
	APP.controls.target.set( APP.BoundingboxX/2.0 , APP.BoundingboxY/2.0, APP.BoundingboxZ/2.0);
	// APP.renderer.render(APP.scene, APP.camera);
	}

window.CenterYZ = function () {
	APP.camera.up.set(0,0,1);
	APP.camera.position.set( APP.BoundingboxMax*3.0  , APP.BoundingboxY/2.0, APP.BoundingboxZ/2.0);
	APP.camera.lookAt(APP.BoundingboxZ/2.0, APP.BoundingboxY/2.0, APP.BoundingboxX/2.0);
	APP.controls.target.set( APP.BoundingboxX/2.0 , APP.BoundingboxY/2.0, APP.BoundingboxZ/2.0);
	// APP.renderer.render(APP.scene, APP.camera);
	}

window.CenterZX = function () {
	APP.camera.up.set(1,0,0);
	APP.camera.position.set( APP.BoundingboxX/2.0, APP.BoundingboxMax*3.0, APP.BoundingboxZ/2.0);
	APP.camera.lookAt(APP.BoundingboxZ/2.0, APP.BoundingboxY/2.0, APP.BoundingboxX/2.0);
	APP.controls.target.set( APP.BoundingboxX/2.0 , APP.BoundingboxY/2.0, APP.BoundingboxZ/2.0);
	// APP.renderer.render(APP.scene, APP.camera);
	}


window.DirLightX = function (ischecked) {
	if( ischecked == true ) {
  		APP.directionalLight.position.x = APP.BoundingboxX/2.0+APP.BoundingboxMax;
		}
	else {
		APP.directionalLight.position.x = APP.BoundingboxX/2.0-APP.BoundingboxMax;
		}
	// APP.renderer.render(APP.scene, APP.camera);
	}

window.DirLightY = function (ischecked) {
	if( ischecked == true ) {
		APP.directionalLight.position.y = APP.BoundingboxY/2.0+APP.BoundingboxMax;
		}
	else {
		APP.directionalLight.position.y = APP.BoundingboxY/2.0-APP.BoundingboxMax;
		}
	}

window.DirLightZ = function (ischecked) {
	if( ischecked == true ) {
		APP.directionalLight.position.z = APP.BoundingboxZ/2.0+APP.BoundingboxMax;
		}
	else {
		APP.directionalLight.position.z = APP.BoundingboxZ/2.0-APP.BoundingboxMax;
		}
	}
window.FrameOffOn =  function (ischecked) {
		if( ischecked == true ) {
      		addBoundingBox();
   			}
		else {
			removeBoundingBox();
			}
      }


// Draw bounding box
function addBoundingBox() {
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
	boundingbox.translateX( APP.BoundingboxX / 2.0 );
	boundingbox.translateY( APP.BoundingboxY / 2.0 );
	boundingbox.translateZ( APP.BoundingboxZ / 2.0 );
	}

function removeBoundingBox(){
	var obj = APP.scene.getObjectByName('BoundingBox');
	if ( obj != undefined ) {
    		APP.scene.remove(obj);
		}
	APP.BoundingBox = 'Off';
	}

function setBoundingBoxColor(objcolor){
	var obj = APP.scene.getObjectByName('BoundingBox');
	if ( obj != undefined ) {
    	obj.material.color.setHex( objcolor );
		}
	}

