
// The DOJO namespace
var DOJO = DOJO || {};

DOJO.mode = null;
DOJO.modes = {
  pan_zoom:0,
  merge:1,
  split:2,
  adjust:3
};
DOJO.threeD_active = false;
DOJO.link_active = false;
DOJO.mousemove_timeout = null;
DOJO.single_segment = false;

DOJO.onmouse_prevous_leftclick = false;
DOJO.onmouse_present_leftclick = false;


DOJO.init = function() {

  DOJO.viewer = new J.viewer('dojo1');

  var args = parse_args();

  DOJO.viewer.init(function() {

    DOJO.update_slice_number(1);
    // Allows for highlighintg of searched segment
    // Allowing for compatability with Neuroblocks
    if (typeof(args['activeId']) != 'undefined') {

      var id = args['activeId'];
      DOJO.viewer._controller._adjust_mode = 1;
      DOJO.viewer._controller._adjust_id = id;

      DOJO.viewer._controller.activate(id);
      DOJO.viewer._controller.highlight(id);

      DOJO.single_segment = true;

    };

    if (typeof(args['jump']) != 'undefined') {

      var coords = args['jump'].split(',');

      if (coords.length != 3) {

        window.alert('Error parsing position.');

      } else {

        DOJO.viewer._camera._w = 0;
        DOJO.viewer._camera.jumpIJK(coords[0], coords[1], coords[2]);
      }

    };


  });

  DOJO.setup_buttons();

};

DOJO.setup_buttons = function() {

  var threeD = document.getElementById('threeD');
  threeD.style.left = (document.body.clientWidth - 310) + 'px';
  DOJO.make_resizable();

  var merge = document.getElementById('merge');
  var merge_selected = document.getElementById('merge_selected');

  merge.onclick = merge_selected.onclick = function() {

    if (DOJO.mode != DOJO.modes.merge) {

      if (!DOJO.single_segment)
        DOJO.reset_tools();

      merge.style.display = 'none';
      merge_selected.style.display = 'block';

      DOJO.mode = DOJO.modes.merge;

    } else {

      DOJO.reset_tools();

    }

  };

  var split = document.getElementById('split');
  var split_selected = document.getElementById('split_selected');

  split.onclick = split_selected.onclick = function() {

    if (DOJO.mode != DOJO.modes.split) {

      DOJO.reset_tools();

      split.style.display = 'none';
      split_selected.style.display = 'block';

      DOJO.mode = DOJO.modes.split;

    } else {

      DOJO.reset_tools();

    }

  };


  // Adjustは公開APIではなくなったが機能としては存在するのでボタン機能を残しておく
  var adjust = document.getElementById('adjust');
  var adjust_selected = document.getElementById('adjust_selected');

    adjust.onclick = adjust_selected.onclick = function() {
      if (DOJO.mode != DOJO.modes.adjust) {
        DOJO.reset_tools();
        $('#extend_adjust, #extend_adjust_header').show();
        adjust.style.display = 'none';
        adjust_selected.style.display = 'block';
        DOJO.mode = DOJO.modes.adjust;
        //console.log(DOJO.viewer._controller)
		DOJO.viewer._controller.circle_cursor()
        //DOJO.viewer._canvas.style.cursor = iconname; 
      } else {
      	DOJO.viewer._canvas.style.cursor = 'auto';
        DOJO.reset_tools();
        $('#extend_adjust, #extend_adjust_header').hide();
      }

    };

  var threed = document.getElementById('3d');
  var threed_selected = document.getElementById('3d_selected');

  threed.onclick = threed_selected.onclick = function() {

    if (!DOJO.threeD_active) {

      // threed.style.border = '1px solid white';

      threed.style.display = 'none';
      threed_selected.style.display = 'block';

      document.getElementById('threeD').style.display = 'block';

      if (!DOJO.threeD) {
        DOJO.init_threeD();
      }

      DOJO.threeD_active = true;

    } else {

      // threed.style.border = '';
      threed.style.display = 'block';
      threed_selected.style.display = 'none';

      document.getElementById('threeD').style.display = 'none';

      DOJO.threeD_active = false;

      DOJO.threeD.renderer.destroy();

      DOJO.threeD = null;

    }

  };


  //
  // Adds by H Urakubo (19/2/10)
  //

  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  var extend_adjust = document.getElementById('extend_adjust');
  extend_adjust.onmousedown = function(e) {
		// console.log('Anyway, on mouse button')
    	e = e || window.event;
    	e.preventDefault();
    	// get the mouse cursor position at startup:
    	pos3 = e.clientX;
    	pos4 = e.clientY;
    	document.onmouseup = closeDragElement;
    	// call a function whenever the cursor moves:
    	document.onmousemove = elementDrag;
  		}
	elementDrag = function(e) {
		// console.log('elementDrag on Adjust');
    	e = e || window.event;
    	e.preventDefault();
    	// calculate the new cursor position:
    	pos1 = pos3 - e.clientX;
   		pos2 = pos4 - e.clientY;
    	pos3 = e.clientX;
    	pos4 = e.clientY;
    	// set the element's new position:
    	extend_adjust.style.top = (extend_adjust.offsetTop - pos2) + "px";
    	extend_adjust.style.left = (extend_adjust.offsetLeft - pos1) + "px";
  		}
	closeDragElement = function() {
    	// stop moving when mouse button is released:
    	document.onmouseup = null;
    	document.onmousemove = null;
  		}


  var adjust_start_colorbox = document.getElementById('colorbox');
  adjust_start_colorbox.onclick = function() {
  			if (!DOJO.viewer.is_locked(this._adjust_id))
				DOJO.viewer._controller.start_adjust_colorbox()
  		}


  var adjust_start_colorbox = document.getElementById('colorbox2');
  adjust_start_colorbox.onclick = function() {
  			if (!DOJO.viewer.is_locked(this._adjust_id))
				DOJO.viewer._controller.start_adjust_colorbox2()
  		}


  var adjust_start_eraser = document.getElementById('eraser');
  adjust_start_eraser.onclick = function() {
  			if (!DOJO.viewer.is_locked(this._adjust_id))
				DOJO.viewer._controller.start_adjust_eraser()
  		}


  var save = document.getElementById('save');

  save.onclick = function() {

    // if (confirm("Saving might take hours and Dojo will be unusable during this time!\n\nDo you really want to save right now?") == true) {

      $('#blocker').show();
      DOJO.viewer._controller.save();

    // }


  };

  var undo = document.getElementById('undo');

  undo.onclick = function() {

    DOJO.viewer._controller.undo_action();

  };


  var redo = document.getElementById('redo');

  redo.onclick = function() {

    DOJO.viewer._controller.redo_action();

  };



};

DOJO.reset_tools = function() {

  DOJO.mode = DOJO.modes.pan_zoom;

  merge.style.display = 'block';
  merge_selected.style.display = 'none';

  split.style.display = 'block';
  split_selected.style.display = 'none';

  adjust.style.display = 'block';
  adjust_selected.style.display = 'none';

  DOJO.viewer._controller.end();

  // reset 3d view
  DOJO.viewer._controller.reset_fixed_3d_labels();
  DOJO.viewer._controller.reset_3d_labels();

};

DOJO.onleftclick = function(x, y) {

  // get pixel coordinates
  var i_j = DOJO.viewer.xy2ij(x,y);

  if (i_j[0] == -1) {
    DOJO.viewer._controller.reset_fixed_3d_labels();
    DOJO.viewer._controller.reset_3d_labels();
    return;
  }

  DOJO.viewer.get_segmentation_id(i_j[0], i_j[1], function(id) {

    // now we have the segmentation id
    if (DOJO.mode == DOJO.modes.merge) {

      if (!DOJO.viewer.is_locked(id))
        DOJO.viewer._controller.start_merge(id, x, y);
        // DOJO.viewer._controller.merge(id);

    } else if (DOJO.mode == DOJO.modes.split) {

      if (!DOJO.viewer.is_locked(id))
        DOJO.viewer._controller.start_split(id, x, y);

    } else if (DOJO.mode == DOJO.modes.adjust) {

      if (!DOJO.viewer.is_locked(id))
        DOJO.viewer._controller.start_adjust(id, x, y);

    } else {

      if (DOJO.threeD_active) {

        DOJO.viewer._controller._use_3d_labels = true;

        if (!DOJO.viewer._controller.is_3d_label(id)) {
          DOJO.viewer._controller.add_fixed_3d_label(id);
          DOJO.viewer._controller.add_3d_label(id);
        } else {
          DOJO.viewer._controller.remove_fixed_3d_label(id);
          DOJO.viewer._controller.remove_3d_label(id);
        }

      }

    }


  });

};


//
// Mod by H Urakubo
//

DOJO.onmousemove = function(x, y) {

	DOJO.onmouse_present_leftclick = false;
	if (DOJO.viewer._interactor._left_down){
		DOJO.onmouse_present_leftclick = true;
  		if (DOJO.mode == DOJO.modes.split) {
			DOJO.viewer._controller.draw_split(x, y);
		} else if (DOJO.mode == DOJO.modes.adjust) {
			DOJO.viewer._controller.draw_adjust(x, y);
		} else if (DOJO.mode == DOJO.modes.merge) {
			DOJO.viewer._controller.draw_merge(x, y);
		}
	}
	DOJO.onmouse_previous_leftclick = DOJO.onmouse_present_leftclick;
};

DOJO.onmouseup = function(x, y) {

  var i_j = DOJO.viewer.xy2ij(x,y);

  if (DOJO.mode == DOJO.modes.split) {

    DOJO.viewer._controller.end_draw_split(x, y);

  } else if (DOJO.mode == DOJO.modes.merge) {

    DOJO.viewer._controller.end_draw_merge(x,y);

  }

};

DOJO.update_slice_number = function(n) {

  var slicenumber = document.getElementById('slicenumber');
  slicenumber.innerHTML = n-1+'/'+(DOJO.viewer._image.max_z_tiles-1);

  // reset the cursors if we are in collab mode
  if (DOJO.link_active) {
    DOJO.viewer._controller.reset_cursors();
  }

};

DOJO.update_label = function(x, y) {

  var i_j = DOJO.viewer.xy2ij(x,y);

  var label = document.getElementById('label');

  if (i_j[0] == -1) {
    label.innerHTML = ' Label n/a';
    if (DOJO.mode != DOJO.modes.merge)
      DOJO.viewer._controller.reset_3d_labels();
    return;
  }

  DOJO.viewer.get_segmentation_id(i_j[0], i_j[1], function(id) {

    if (!id) return;

    var color = DOJO.viewer.get_color(id);
    var color_hex = rgbToHex(color[0], color[1], color[2]);

    label.innerHTML = ' Label <font color="' + color_hex + '">' + id + '</font> (' + i_j[0] + ',' + i_j[1] + ')';

    DOJO.viewer._controller.highlight(id);

  });

};

DOJO.update_log = function(input) {
    var log = document.getElementById('log');

  var m = input.value;

  var color1 = DOJO.viewer.get_color(input.id+100);
  var color1_hex = rgbToHex(color1[0], color1[1], color1[2]);

  m = m.replace('$USER', '<font color="'+color1_hex+'">'+input.origin+'</font>');

  // add timestamp
  var message = timestamp() + ' ' + m;

  log.innerHTML = message + '<br>' + log.innerHTML;

};

DOJO.make_resizable = function() {

// Using DragResize is simple!
// You first declare a new DragResize() object, passing its own name and an object
// whose keys constitute optional parameters/settings:

var dragresize = new DragResize('dragresize',
 { handles: ['bl'], minWidth: 300, minHeight: 300, minLeft: 10, minTop: 10, minRight: 10, minBottom: 10 });

// Optional settings/properties of the DragResize object are:
//  enabled: Toggle whether the object is active.
//  handles[]: An array of drag handles to use (see the .JS file).
//  minWidth, minHeight: Minimum size to which elements are resized (in pixels).
//  minLeft, maxLeft, minTop, maxTop: Bounding box (in pixels).

// Next, you must define two functions, isElement and isHandle. These are passed
// a given DOM element, and must "return true" if the element in question is a
// draggable element or draggable handle. Here, I'm checking for the CSS classname
// of the elements, but you have have any combination of conditions you like:

dragresize.isElement = function(elm)
{
 if (elm.className && elm.className.indexOf('draggable_panel') > -1) return true;
};
dragresize.isHandle = function(elm)
{
 if (elm.className && elm.className.indexOf('drsMoveHandle') > -1) return true;
};

// You can define optional functions that are called as elements are dragged/resized.
// Some are passed true if the source event was a resize, or false if it's a drag.
// The focus/blur events are called as handles are added/removed from an object,
// and the others are called as users drag, move and release the object's handles.
// You might use these to examine the properties of the DragResize object to sync
// other page elements, etc.

dragresize.ondragfocus = function() { };
dragresize.ondragstart = function(isResize) { };
dragresize.ondragmove = function(isResize) { if (DOJO.threeD) DOJO.threeD.renderer.onResize(); };
dragresize.ondragend = function(isResize) { };
dragresize.ondragblur = function() { };

// Finally, you must apply() your DragResize object to a DOM node; all children of this
// node will then be made draggable. Here, I'm applying to the entire document.
dragresize.apply(document);



};

DOJO.init_threeD = function() {

  DOJO.threeD = DOJO.threeD || {};

  // create and initialize a 3D renderer
  var r = new X.renderer3D();
  r.container = 'threeDcontent';
  r.init();

  DOJO.threeD.renderer = r;

  var vol = new X.volume();
  var zSample_num = Math.min(DOJO.viewer._image.zSample_max,DOJO.viewer._image.max_z_tiles);
  var volume_zoomlevel = pad(DOJO.viewer._image.zoomlevel_count - 1, 8);

  vol.spacing = [1,1,7.5];
  vol.dimensions = [512,512,zSample_num];
  vol.file = '/image/volume/'+volume_zoomlevel+'/&.RZ';
  vol.xySampleRate = 1;

  vol.labelmap.use32bit = true;
  vol.labelmap.file = '/segmentation/volume/'+volume_zoomlevel+'/&.RZ';
  vol.labelmap.dimensions = vol.dimensions;
  vol.labelmap.opacity = .5;

//  vol.labelmap._dirty = true;

  DOJO.threeD.volume = vol;
  DOJO.threeD.renderer = r;

  DOJO.viewer._controller.update_threeD();

  r.add(vol);
  // r.add(s)


  var box = new X.object();
  box.points = new X.triplets(72);
  box.normals = new X.triplets(72);
  box.type = 'LINES';
  var _x = vol.dimensions[0]*vol.spacing[0] / 2;
  var _y = vol.dimensions[1]*vol.spacing[1] / 2;
  var _z = vol.dimensions[2]*vol.spacing[2] / 2;
  box.points.add(_x, -_y, _z);
  box.points.add(-_x, -_y, _z);
  box.points.add(_x, _y, _z);
  box.points.add(-_x, _y, _z);
  box.points.add(_x, -_y, -_z);
  box.points.add(-_x, -_y, -_z);
  box.points.add(_x, _y, -_z);
  box.points.add(-_x, _y, -_z);
  box.points.add(_x, -_y, _z);
  box.points.add(_x, -_y, -_z);
  box.points.add(-_x, -_y, _z);
  box.points.add(-_x, -_y, -_z);
  box.points.add(_x, _y, _z);
  box.points.add(_x, _y, -_z);
  box.points.add(-_x, _y, _z);
  box.points.add(-_x, _y, -_z);
  box.points.add(_x, _y, _z);
  box.points.add(_x, -_y, _z);
  box.points.add(-_x, _y, _z);
  box.points.add(-_x, -_y, _z);
  box.points.add(-_x, _y, -_z);
  box.points.add(-_x, -_y, -_z);
  box.points.add(_x, _y, -_z);
  box.points.add(_x, -_y, -_z);
  for ( var i = 0; i < 24; ++i) {
    box.normals.add(0, 0, 0);
  }
  r.add(box);

  var slice = new X.object();
  slice.points = new X.triplets(24);
  slice.normals = new X.triplets(24);
  slice.type = 'LINES';
  slice.points.add(_x, _y, 0);
  slice.points.add(-_x, _y, 0);
  slice.points.add(_x, _y, 0);
  slice.points.add(_x, -_y, 0);
  slice.points.add(_x, -_y, 0);
  slice.points.add(-_x, -_y, 0);
  slice.points.add(-_x, _y, 0);
  slice.points.add(-_x, -_y, 0);
  slice.color = [1,0,0];
  for ( var i = 0; i < 8; ++i) {
    slice.normals.add(0, 0, 0);
  }
  slice.transform.translateZ(-vol.dimensions[2]/2*vol.spacing[2]);
  r.add(slice);

  DOJO.threeD.slice = slice;

  r.camera.position = [-100,-400,-700]

  r.render(); // ..and render it

  r.onShowtime = function() {

    vol.volumeRendering = true;
    vol.opacity = 0.5;

    // we also need to redraw the problem table
    DOJO.viewer._controller.redraw_exclamationmarks();

  }

  r.interactor.onMouseDown = function() {

    this._touch_started = Date.now();

  }

  r.interactor.onMouseUp = function() {

    this._touch_ended = Date.now();

    if (typeof this._touch_started == 'undefined') {
      this._touch_started = this._touch_ended;
    }

    if (this._touch_ended - this._touch_started < 200) {
      var m = r.interactor.mousePosition;
      var id = r.pick(m[0], m[1]);
      if (id > 0){
        var o = r.get(id);

        if (id) {
          DOJO.viewer._controller.pick3d(o);
        }

      }
      // var o2 = r.pick3d(m[0], m[1], null, null, box);

    }

  }

};

DOJO.save = function() {

  DOJO.viewer._controller.save();

};
