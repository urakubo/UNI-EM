var J = J || {};

J.viewer = function(container) {

  this._container = document.getElementById(container);

  this._canvas = document.createElement('canvas');
  this._canvas.width = this._container.clientWidth;
  this._canvas.height = this._container.clientHeight;
  this._container.appendChild(this._canvas);

  this._width = this._canvas.width;
  this._height = this._canvas.height;

  this._context = this._canvas.getContext('2d');

  this._image_buffer = document.createElement('canvas');
  this._image_buffer_context = this._image_buffer.getContext('2d');
  this._image_buffer_ready = false;

  this._overlay_buffer = document.createElement('canvas');
  this._overlay_buffer_context = this._overlay_buffer.getContext('2d');

  this._segmentation_buffer = document.createElement('canvas');
  this._segmentation_buffer.width = 512;
  this._segmentation_buffer.height = 512;
  this._segmentation_buffer_context = this._segmentation_buffer.getContext('2d');
  this._pixel_data_buffer = this._segmentation_buffer_context.createImageData(512, 512);

  this._offscreen_buffer = document.createElement('canvas');
  this._container.appendChild(this._offscreen_buffer);
  this._offscreen_buffer.width = 512;
  this._offscreen_buffer.height = 512;

  // Buffer for the mouse pointer
  this._pt_g_cols = [[0,0],[.5,0],[.6,.1],[.7,.2],[.8,1],[1,0]];
  this._pt_buff = document.createElement('canvas');
  this._container.appendChild(this._pt_buff);
  this._pt_ctx = this._pt_buff.getContext('2d');
  this._pt_ctx.rad = 200;

  this._force_rerender = false;

  this._image = null;
  this._segmentation = null;

  this._colormap = null;
  this._gl_colormap = null;
  this._max_colors = 0;

  this._overlay_show = true;
  this._overlay_opacity = 100;
  this._overlay_borders = true;
  this._only_locked = false;

  this._loader = new J.loader(this);
  this._camera = new J.camera(this);
  this._controller = new J.controller(this);
  this._offscreen_renderer = new J.offscreen_renderer(this);

  this._webgl_supported = true;
  this._drawer = null;

  if (!this._offscreen_renderer.init('vs1', 'fs1')) {
    console.log('No WebGL support.');

    // hide the 3d icon
    document.getElementById('3d').style.display = 'none';

    this._webgl_supported = false;
  }

};

J.viewer.prototype.init = function(callback) {

  // check which drawer to use (WebGL vs. canvas)
  if (this._webgl_supported) {
    this._drawer = this.draw_webgl.bind(this);
  } else {
    this._drawer = this.draw_canvas.bind(this);
  }


  // get contents
  this._loader.load_json('/image/contents', function(res) {

    this._image = JSON.parse(res.response);

    // type cast some stuff
    this._image.width = parseInt(this._image.width, 10);
    this._image.height = parseInt(this._image.height, 10);

    this._image.zSample_max = parseInt(this._image.zSample_max, 10);
    this._image.max_z_tiles = parseInt(this._image.max_z_tiles, 10);
    this._image.zoomlevel_count = parseInt(this._image.zoomlevel_count, 10);
    this._camera._zStack = this._image.zSample_max/this._image.max_z_tiles;

    this._image.zoom_levels = this.calc_zoomlevels();

    // set to default zoom level (smallest in MOJO notation)
    this._camera._w = this._image.zoomlevel_count - 1;

    this._interactor = new J.interactor(this);

    this._image_buffer.width = this._overlay_buffer.width = this._pt_buff.width = this._image.width;
    this._image_buffer.height = this._overlay_buffer.height = this._pt_buff.height = this._image.height;

    this._loader.load_json('/segmentation/contents', function(res) {

      this._segmentation = JSON.parse(res.response);

      // TODO support if we don't have a segmentation
      this._loader.load_json('/segmentation/colormap', function(res) {

        this._colormap = JSON.parse(res.response);
        this._max_colors = this._colormap.length;
        this._gl_colormap = new Uint8Array(3*this._max_colors);

        var pos = 0;
        for (var i=0; i<this._max_colors; i++) {

          var c = this._colormap[i];

          this._gl_colormap[pos++] = c[0];
          this._gl_colormap[pos++] = c[1];
          this._gl_colormap[pos++] = c[2];

/*
		console.log(c[0])
		console.log(c[1])
		console.log(c[2])
*/

        }

        this._camera.reset();

        // start rendering loop
        this.render();

        // now create websocket connection
        this._websocket = new J.websocket(this);

        callback();

      }.bind(this)); // /segmentation/colormap

    }.bind(this)); // load /segmentation/contents

  }.bind(this)); // load /image/contents

};

J.viewer.prototype.calc_zoomlevels = function() {

  var zoom_levels = [];

  // largest zoom level
  zoom_levels[0] = [Math.ceil(this._image.width/512), Math.ceil(this._image.height/512), this._image.width/512, this._image.height/512];

  var _width = this._image.width/2;
  var _height = this._image.height/2;

  for (var w=1; w<this._image.zoomlevel_count; w++) {

    var level_x_count = Math.ceil(_width / 512);
    var level_y_count = Math.ceil(_height / 512);

    zoom_levels[w] = [level_x_count, level_y_count, _width / 512, _height / 512];

    _width /= 2;
    _height /= 2;

  }

  return zoom_levels;

};

J.viewer.prototype.redraw = function() {

  // trigger re-draw
  this.loading(true);

  this._loader.load_tiles(this._camera._x, this._camera._y, this._camera._z, this._camera._w, this._camera._w, false);

};

J.viewer.prototype.rerender = function() {

  this._force_rerender = true;

};

J.viewer.prototype.draw_image = function(x,y,z,w,i,s) {

  this._drawer(x,y,z,w,i,s);

};

J.viewer.prototype.draw_webgl = function(x,y,z,w,i,s) {

  // draw image and segmentation
  this._offscreen_renderer.draw(i, s, this._image_buffer_context, x, y);

};

J.viewer.prototype.draw_canvas = function(x,y,z,w,i,s) {

  this._image_buffer_context.drawImage(i,0,0,512,512,x*512,y*512,512,512);

  if (!this._overlay_show) {
    // nothing more here
    return;
  }

  // draw segmentation
  var pixel_data = this._pixel_data_buffer;
  var pixel_data_data = pixel_data.data;
  var segmentation_data = new Uint32Array(s.buffer);

  var opacity = this._overlay_opacity;
  var highlighted_id = this._controller._highlighted_id;
  var activated_id = this._controller._activated_id;

  var split_mode = this._controller._split_mode;
  var adjust_mode = this._controller._adjust_mode;

  var pos = 0; // running pixel (rgba) index, increases by 4
  var max_colors = this._max_colors;
  var colormap = this._colormap;

  var right_border = 1;
  var left_border = 0;

  var i = 0;
  var j = 0;

  // run through all 512*512 bytes
  for (var p=0; p<262144; p++) {

    i++;
    if (i == 512) {
      i = 0;
      j++;
    }

    var id = this.lookup_id(segmentation_data[p]);

    var color = this.get_color(id);

    if (this.is_locked(id)) {

      var striped = (i/512 % 0.05 < 0.01) || (j/512 % 0.05 < 0.01);

      if (striped) {

        pixel_data_data[pos++] = color[0] - 70;
        pixel_data_data[pos++] = color[1] - 70;
        pixel_data_data[pos++] = color[2] - 70;
        pixel_data_data[pos++] = opacity;

      } else {

        pixel_data_data[pos++] = color[0];
        pixel_data_data[pos++] = color[1];
        pixel_data_data[pos++] = color[2];
        pixel_data_data[pos++] = 0.3*255;

      }

    } else if (adjust_mode > 0 && id != activated_id) {

      pixel_data_data[pos++] = 0;
      pixel_data_data[pos++] = 0;
      pixel_data_data[pos++] = 0;
      pixel_data_data[pos++] = 0;

    } else if (split_mode > 0 && id == activated_id) {

      pixel_data_data[pos++] = 0;
      pixel_data_data[pos++] = 0;
      pixel_data_data[pos++] = 0;
      pixel_data_data[pos++] = 0;

    } else {

      pixel_data_data[pos++] = color[0];
      pixel_data_data[pos++] = color[1];
      pixel_data_data[pos++] = color[2];

      if (id == highlighted_id || id == activated_id) {
        pixel_data_data[pos++] = 200;
      } else {
        pixel_data_data[pos++] = opacity;
      }

    }

  }

  this._segmentation_buffer_context.putImageData(pixel_data, 0, 0);
  this._image_buffer_context.drawImage(this._segmentation_buffer,0,0,512,512,x*512,y*512,512,512);

};

J.viewer.prototype.lookup_id = function(id) {

  if (!this._controller._new_merge_table) return;

  // check if this has an entry in the merge table
  while(typeof this._controller._new_merge_table[id] !== 'undefined') {
    id = this._controller._new_merge_table[id];
  }

  return id;

};

J.viewer.prototype.get_color = function(id) {

  return this._colormap[id % this._max_colors];

};

J.viewer.prototype.move_pointer = function(x,y,win = true) {

  // Get zoom level and radius
  var level = 1/(Math.pow(2,this._camera._w));
  var rad = this._pt_ctx.rad*level;
  this.clear_pointer_buffer();

  // If screen coordinates
  if (win) {
    var i_j = this.xy2ij(x,y);
    if (i_j.some((e) => {return e < 0})) { return; };
    i_j = i_j.map((e) => {return e*level});
  }
  else {
    var i_j = [x,y];
  }

  var pt =rad*(1-this._pt_g_cols[4][0]);
  var grad = this._pt_ctx.createRadialGradient(i_j[0], i_j[1], 0, i_j[0], i_j[1],rad);

  this._pt_g_cols.forEach((c)=>{grad.addColorStop(c[0], 'rgba(1,1,1,'+c[1]+')');});
  this._pt_ctx.arc(i_j[0], i_j[1],rad, 0, 2*Math.PI);
  this._pt_ctx.fillStyle = grad;
  this._pt_ctx.fill();

  this._pt_ctx.beginPath();
  this._pt_ctx.fillStyle = 'rgb(1,1,1)';
  this._pt_ctx.moveTo(i_j[0]-pt/2,i_j[1]+pt-rad);
  this._pt_ctx.lineTo(i_j[0]+pt/2,i_j[1]+pt-rad);
  this._pt_ctx.lineTo(i_j[0],i_j[1]);
  this._pt_ctx.closePath();
  this._pt_ctx.fill();
};

J.viewer.prototype.clear_buffer = function(width, height) {

  this._image_buffer_context.clearRect(0, 0, width, height);

};

J.viewer.prototype.clear_overlay_buffer = function() {

  this._overlay_buffer_context.clearRect(0,0,this._image.width, this._image.height);

};

J.viewer.prototype.clear_pointer_buffer = function() {

  this._pt_ctx.clearRect(0,0,this._image.width, this._image.height);

};

J.viewer.prototype.clear = function() {

  var _width = this._width;
  var _height = this._height;

  this._context.save();
  this._context.setTransform(1, 0, 0, 1, 0, 0);
  this._context.clearRect(0, 0, _width, _height);
  this._context.restore();

};

J.viewer.prototype.toggle_borders = function() {
  this._overlay_borders = !this._overlay_borders;
  this.redraw();
};

J.viewer.prototype.toggle_segmentation = function() {
  this._overlay_show = !this._overlay_show;
  this.redraw();
};

J.viewer.prototype.increase_opacity = function() {

  this._overlay_opacity = Math.min(255, this._overlay_opacity+=20);
  this.redraw();

};

J.viewer.prototype.decrease_opacity = function() {

  this._overlay_opacity = Math.max(0, this._overlay_opacity-=20);
  this.redraw();

};

J.viewer.prototype.loading = function(value) {
    this._image_buffer_ready = !value;
};

J.viewer.prototype.render = function() {

  this._context.setTransform(this._camera._view[0], this._camera._view[1], this._camera._view[3], this._camera._view[4], this._camera._view[6], this._camera._view[7]);

  if (this._image_buffer_ready || this._force_rerender) {

    if (this._force_rerender) console.log('rerender')

    this.clear();
    // put image buffer
    this._context.drawImage(this._image_buffer, 0, 0);

    // draw overlays
    this._context.drawImage(this._overlay_buffer,0,0);

    // draw mouse pointer
    this._context.drawImage(this._pt_buff,0,0);

    this._force_rerender = false;
  }

  this._AnimationFrameID = window.requestAnimationFrame(this.render.bind(this));

};

J.viewer.prototype.xy2uv = function(x, y) {

  var u = x - this._camera._view[6];
  var v = y - this._camera._view[7];
  if (u < 0 || u >= this._camera._view[0] * this._image.zoom_levels[this._camera._w][2] *512) {
    u = -1;
  }

  if (v < 0 || v >= this._camera._view[4] * this._image.zoom_levels[this._camera._w][3] *512) {
    v = -1;
  }

  return [u, v];

};

J.viewer.prototype.uv2xy = function(u, v) {

  return [u + this._camera._view[6], v + this._camera._view[7]];

};

// returns the pixel coordinates looking at the largest image
J.viewer.prototype.xy2ij = function(x, y) {

  var u_v = this.xy2uv(x, y);

  if (u_v[0] == -1 || u_v[1] == -1) {
    return [-1, -1];
  }

  var i_j = [Math.floor(((u_v[0]/this._image.zoom_levels[this._camera._w][2])*this._image.zoom_levels[0][2])/this._camera._view[0]),
             Math.floor(((u_v[1]/this._image.zoom_levels[this._camera._w][3])*this._image.zoom_levels[0][3])/this._camera._view[4])];

  return i_j;

};

J.viewer.prototype.ij2xy = function(i, j) {

  var u = ((i * this._camera._view[0])/this._image.zoom_levels[0][2]) * this._image.zoom_levels[this._camera._w][2];
  var v = ((j * this._camera._view[4])/this._image.zoom_levels[0][3]) * this._image.zoom_levels[this._camera._w][3];


  return this.uv2xy(u, v);

};

J.viewer.prototype.ij2uv = function(i, j) {

  var u = ((i * this._camera._view[0])/this._image.zoom_levels[0][2]) * this._image.zoom_levels[this._camera._w][2];
  var v = ((j * this._camera._view[4])/this._image.zoom_levels[0][3]) * this._image.zoom_levels[this._camera._w][3];

  return [u,v];

};

J.viewer.prototype.ij2uv_no_zoom = function(i, j) {

  var u = ((i)/this._image.zoom_levels[0][2]) * this._image.zoom_levels[this._camera._w][2];
  var v = ((j)/this._image.zoom_levels[0][3]) * this._image.zoom_levels[this._camera._w][3];

  return [u,v];

};

J.viewer.prototype.ijk2xyz = function(i, j, k) {

  var spacing = 1;
  return [Math.floor((i*512)/this._image.height) - 256, Math.floor((j*512)/this._image.width) - 256, Math.floor(k - (this._image.max_z_tiles-1)/2)*spacing];

};

J.viewer.prototype.ijk2xyz3d = function(i, j, k) {

  var spacing = 1;

  if (DOJO.threeD) {
    spacing = DOJO.threeD.volume.spacing[2];
  }

  return [Math.floor((i*512)/this._image.height) - 256, Math.floor((j*512)/this._image.width) - 256, Math.floor(k - (this._image.max_z_tiles-1)/2)*spacing];

};


J.viewer.prototype.xyz2ijk = function(x, y, z) {

  var i = Math.floor((x + 256)*this._image.height/512);
  var j = Math.floor((y + 256)*this._image.width/512);
  var k = z/DOJO.threeD.volume.spacing[2] + Math.floor(this._image.max_z_tiles/2);

  return [i, j, k];

};

J.viewer.prototype.get_segmentation_id = function(i, j, callback) {

  var x = Math.floor(i / 512);
  var y = Math.floor(j / 512);
  var z = this._camera._z;
  var w = 0;

  this._loader.get_segmentation(x, y, z, w, function(s) {

    var pixel_data = new Uint32Array(s.buffer);

    var id = this.lookup_id(pixel_data[(j % 512) * 512 + (i % 512)]);

    callback(id);

  }.bind(this));

};

J.viewer.prototype.get_segmentation_id_before_merge = function(i, j, callback) {

  var x = Math.floor(i / 512);
  var y = Math.floor(j / 512);
  var z = this._camera._z;
  var w = 0;

  this._loader.get_segmentation(x, y, z, w, function(s) {

    var pixel_data = new Uint32Array(s.buffer);

    var id = pixel_data[(j % 512) * 512 + (i % 512)];

    callback(id);

  }.bind(this));

};

J.viewer.prototype.is_locked = function(id) {
  return this._controller.is_locked(id);
};
