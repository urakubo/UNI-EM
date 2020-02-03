import { APP } from "./APP";
//
//
//
window.BackgroundWhiteBlack = function (ischecked) {
		if( ischecked == true ) {
			APP.setBackGroundColor( 0x000000 );
			APP.BackGroundColor = 'Black';
			APP.setBoundingBoxColor( 0xffffff );
   			}
		else {
		    APP.setBackGroundColor( 0xffffff );
      		APP.BackGroundColor = 'White';
      		APP.setBoundingBoxColor( 0x000000 );
			}
      }
window.FrameOffOn =  function (ischecked) {
		if( ischecked == true ) {
      		APP.addBoundingBox();
   			}
		else {
			APP.removeBoundingBox();
			}
      }
window.DirLight = function (isnum) {
		APP.directionalLight.intensity = isnum / 100;
      }
window.AmbLight = function (isnum) {
		APP.ambientLight.intensity = isnum / 100;
      }

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

