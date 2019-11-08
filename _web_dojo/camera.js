var J = J || {};

J.camera = function(viewer) {

  this._viewer = viewer;
  this._loader = this._viewer._loader;
  // Initialize empty variables
  this._zStack = 1;
  this._x = 0;
  this._y = 0;
  this._z = 0;
  this._w = 1;

  // we need to cache this here since manipulations to the camera matrix might mess things up
  this._i_j = [0, 0];

  // a c e
  // b d f
  // 0 0 1
  this._view = [1, 0, 0, 0, 1, 0, 0, 0, 1];

  this._linear_zoom_factor = 0.3;

  this._zoom_end_timeout = null;

};


J.camera.prototype.center = function() {

  this._view[6] = this._viewer._width/2 - 512/2;
  this._view[7] = this._viewer._height/2 - 512/2;

};

J.camera.prototype.auto_scale = function() {

  // var _w_scale = this._viewer._width / 512*this._viewer._zoom_level;
  // var _h_scale = this._viewer._height / 512*this._viewer._zoom_level;

  // var _auto_scale = parseInt(Math.min(_w_scale, _h_scale),10);

  // this._view[0] = _auto_scale;
  // this._view[4] = _auto_scale;

};

J.camera.prototype.reset = function() {

  this.auto_scale();
  this.center();

};

J.camera.prototype.zoom_end = function() {

  // this._loader.load_tiles(this._x, this._y, this._z, this._w, this._w, false);



};

J.camera.prototype.jump = function(i, j, k) {

  this._z = k;
  var x_y_z = this._viewer.ijk2xyz(i, j, k);
  if (DOJO.threeD) {
    x_y_z = this._viewer.ijk2xyz3d(i, j, k);
    DOJO.threeD.slice.transform.matrix[14] = x_y_z[2];
  }
  DOJO.update_slice_number(parseInt(k,10)+1);
  this._loader.load_tiles(i, j, k, this._w, this._w, false);

};



J.camera.prototype.jumpIJK = function(i, j, k) {

  var shape = [['width', i, 0], ['height', j, 0], ['max_z_tiles', k, 1]],
  ijk_int = [], ijk_str = [], w = this._w, image = this._viewer._image, view = this._view;

  shape.forEach( function(s) {
    ijk_int.push( Math.min(this[s[0]]-s[2], Math.max(0, parseInt(s[1],10))) );
    ijk_str.push( ijk_int.slice(-1)[0].toString() );
    }, image);

  this._z = ijk_str[2];
  DOJO.update_slice_number(ijk_int[2]+1);
  this._viewer._camera._i_j = ijk_str.slice(0,2);
  var level = 1/(Math.pow(2,w));

  // Moves the camera to the appropriate horizontal coordinate
  ijk_int = ijk_int.slice(0,2).map((e) => { return level*e; });
  this._loader.load_tiles.apply(this._loader,ijk_str.concat([w, w, false]));
  this._view[6] = this._viewer._width/2 - view[0]*ijk_int[0]
  this._view[7] = this._viewer._height/2 - view[4]*ijk_int[1]

  // control mouse pointer
  // DOJO.viewer.move_pointer(ijk_int[0],ijk_int[1],false);

};



///
J.camera.prototype.zoom = function(x, y, delta) {

  // don't zoom when using adjust or split
  if (this._viewer._controller._split_mode != -1 && this._viewer._controller._split_mode != 666) return;
  if (this._viewer._controller._adjust_mode != -1 && !DOJO.single_segment) return;

  // perform linear zooming until a new image zoom level is reached
  // then reset scale to 1 and show the image

  this._viewer._controller.clear_exclamationmarks();
  this._viewer._controller.reset_cursors();

  var u_v = this._viewer.xy2uv(x,y);

  // only do stuff if we are over the image data
  if (u_v[0] == -1 || u_v[1] == -1) {
    return;
  }

  if (this._zoom_end_timeout) clearTimeout(this._zoom_end_timeout);

  var wheel_sign = sign(delta);

  var future_w = this._w - wheel_sign;
  var future_zoom_level = this._view[0] + Math.round((this._view[0] * wheel_sign * this._linear_zoom_factor)*10)/10;

  // clamp the linear pixel zoom
  if (future_zoom_level <= .5 || future_zoom_level >= 10.0) return;

  var load = false;
  var no_draw = false;

  var old_scale = this._view[0];

  // perform pixel zooming
  this._view[0] = future_zoom_level;
  this._view[4] = future_zoom_level;

  var new_scale = future_zoom_level;

  // here we check if we pass an image zoom level, if yes we need to draw other tiles
  if ((new_scale >= 2 && wheel_sign > 0) || (new_scale-this._linear_zoom_factor < 1 && wheel_sign < 0)) {

    future_zoom_level = this._w - wheel_sign;
    // clamp zooming
    if (future_zoom_level >= 0 && future_zoom_level < this._viewer._image.zoomlevel_count) {

      // this._viewer.loading(true);

      // this time we really draw (no_draw = false)
      load = true;

      // Change zoom level
      this._w = future_zoom_level;

      if (wheel_sign < 0) {

        // zooming out
        old_scale *= 2;
        new_scale *= 2;

      } else {

        // zooming in
        new_scale /= 2;
        old_scale /= 2;

      }

      this._view[0] = new_scale;
      this._view[4] = new_scale;
    }
  }

  u_new = u_v[0]/old_scale * new_scale;
  v_new = u_v[1]/old_scale * new_scale;

  // translate to correct point
  this._view[6] -= wheel_sign * Math.abs(u_v[0] - u_new);
  this._view[7] -= wheel_sign * Math.abs(u_v[1] - v_new);

  if (load) {
    this._loader.load_tiles(x, y, this._z, this._w, future_zoom_level, no_draw);
    // Also move the cursor!
	// this._viewer.move_pointer(x,y);
  }

  this._zoom_end_timeout = setTimeout(this.zoom_end.bind(this), 60);
	
	//
	// Adds by HU 19/2/10
	//
	if (DOJO.mode == DOJO.modes.adjust)	DOJO.viewer._controller.circle_cursor();
};

J.camera.prototype.pan = function(dx, dy) {

  this._view[6] += dx;
  this._view[7] += dy;

  this._viewer._controller.clear_exclamationmarks();
  this._viewer._controller.reset_cursors();

  this._loader.load_tiles(this._x, this._y, this._z, this._w, this._w, false);

};

J.camera.prototype.slice_up = function() {

  if (this._z == this._viewer._image.max_z_tiles-1) return;

  // dont slice when using tools
  if (this._viewer._controller._split_mode != -1 && this._viewer._controller._split_mode != 666) return;
  if (this._viewer._controller._adjust_mode != -1 && !DOJO.single_segment) return;

  this._viewer._controller.clear_exclamationmarks();
  this._viewer._controller.reset_cursors();

  this._viewer.loading(true);
  this._loader.load_tiles(this._x, this._y, ++this._z, this._w, this._w, false);

  if (DOJO.threeD)
    DOJO.threeD.slice.transform.translateZ(DOJO.threeD.volume.spacing[2]*this._zStack);

  DOJO.update_slice_number(this._z+1);

};

J.camera.prototype.slice_down = function() {

  if (this._z == 0) return;

  // dont slice when using tile tools
  if (this._viewer._controller._split_mode != -1 && this._viewer._controller._split_mode != 666) return;
  if (this._viewer._controller._adjust_mode != -1 && !DOJO.single_segment) return;

  this._viewer._controller.clear_exclamationmarks();
  this._viewer._controller.reset_cursors();

  this._viewer.loading(true);
  this._loader.load_tiles(this._x, this._y, --this._z, this._w, this._w, false);

  if (DOJO.threeD)
    DOJO.threeD.slice.transform.translateZ(-DOJO.threeD.volume.spacing[2]*this._zStack);

  DOJO.update_slice_number(this._z+1);

};

