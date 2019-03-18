// Make the DIV element draggable:
var ExtendAdjust = ExtendAdjust || {};


function dragElement(elmnt) {
	console.log('dragElement1 on Adjust');
  	var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    document.getElementById("mydiv1header").onmousedown = ExtendAdjust.dragMouseDown;

	ExtendAdjust.dragMouseDown = function(e) {
		console.log('dragMouseDown on Adjust');
    	e = e || window.event;
    	e.preventDefault();
    	// get the mouse cursor position at startup:
    	pos3 = e.clientX;
    	pos4 = e.clientY;
    	document.onmouseup = ExtendAdjust.closeDragElement;
    	// call a function whenever the cursor moves:
    	document.onmousemove = ExtendAdjust.elementDrag;
  		}

	ExtendAdjust.elementDrag = function(e) {
		console.log('elementDrag on Adjust');
    	e = e || window.event;
    	e.preventDefault();
    	// calculate the new cursor position:
    	pos1 = pos3 - e.clientX;
   		pos2 = pos4 - e.clientY;
    	pos3 = e.clientX;
    	pos4 = e.clientY;
    	// set the element's new position:
    	elmnt.style.top = (ExtendAdjust.elmnt.offsetTop - pos2) + "px";
    	elmnt.style.left = (ExtendAdjust.elmnt.offsetLeft - pos1) + "px";
  		}

	ExtendAdjust.closeDragElement = function() {
    	// stop moving when mouse button is released:
    	document.onmouseup = null;
    	document.onmousemove = null;
  		}

  }

