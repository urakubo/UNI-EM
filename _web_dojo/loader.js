var J = J || {};

J.loader = function(viewer) {

  this._viewer = viewer;

  this._image_cache = [];
  this._segmentation_cache = [];

  this._z_cache_size = 0;

  this._image_loading = [];

};

J.loader.prototype.load_json = function(url, callback) {

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);

  xhr.onload = callback.bind(this, xhr);

  xhr.send(null);

};

J.loader.prototype.load_image = function(x, y, z, w, callback) {
  var i = new Image();
  i.src = '/image/'+pad(z,8)+'/'+w+'/'+x+'_'+y+'.jpg';
  i.onload = callback.bind(this, i);

};

J.loader.prototype.load_segmentation = function(x, y, z, w, callback) {
//  var zlc = this._viewer._image.zoomlevel_count
//  var zoom = Array(w).fill(w).join('')+Array(zlc-w).fill(' ').join('')
//  console.log('  S'+' zoom: '+zoom+'@ '+[x,y,z].join())
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/segmentation/'+pad(z,8)+'/'+w+'/'+x+'_'+y+'.raw', true);
  xhr.responseType = 'arraybuffer';

  xhr.onload = callback.bind(this, xhr);

  xhr.send(null);

};

J.loader.prototype.get_image = function(x, y, z, w, callback, no_cache) {

  // check if we have a cached version
  if (this._image_cache[z]) {

    if (this._image_cache[z][w]) {
      if (this._image_cache[z][w][x]) {
        if (this._image_cache[z][w][x][y]) {
          // we have it cached
          var i = this._image_cache[z][w][x][y];

          if (!no_cache) {
            this.cache_image(x, y, z, w);
          }

          callback(i);

          return;
        }
      }
    }

  }

  this.load_image(x, y, z, w, function(i) {

    // cache this image
    this._image_cache[z] = this._image_cache[z] ? this._image_cache[z] : [];
    this._image_cache[z][w] = this._image_cache[z][w] ? this._image_cache[z][w] : [];
    this._image_cache[z][w][x] = this._image_cache[z][w][x] ? this._image_cache[z][w][x] : [];
    this._image_cache[z][w][x][y] = i;

    // call real callback
    callback(i);

  });

  if (!no_cache) {
    this.cache_image(x, y, z, w);
  }

};

J.loader.prototype.cache_image = function(x, y, z, w) {
  // now get some more images
  for (var j=1;j<=this._z_cache_size;j++) {
    if (z+j < this._viewer._image.max_z_tiles) {
      this.get_image(x, y, z+j, w, function(i) {
              }, true);
    }
  }

};

J.loader.prototype.get_segmentation = function(x, y, z, w, callback, no_cache) {

  // check if we have a cached version
  if (this._segmentation_cache[z]) {

    if (this._segmentation_cache[z][w]) {
      if (this._segmentation_cache[z][w][x]) {
        if (this._segmentation_cache[z][w][x][y]) {
          // we have it cached
          var i = this._segmentation_cache[z][w][x][y];

          callback(i);

          return;
        }
      }
    }

  }

  this.load_segmentation(x, y, z, w, function(s) {

    tempA = s.responseURL.split("/").slice(-3);
    // uncompress
    var compressed = new Zlib.Inflate(new Uint8Array(s.response));
    var raw_s = compressed.decompress();

    // cache this image
    this._segmentation_cache[z] = this._segmentation_cache[z] ? this._segmentation_cache[z] : [];
    this._segmentation_cache[z][w] = this._segmentation_cache[z][w] ? this._segmentation_cache[z][w] : [];
    this._segmentation_cache[z][w][x] = this._segmentation_cache[z][w][x] ? this._segmentation_cache[z][w][x] : [];
    this._segmentation_cache[z][w][x][y] = raw_s;

    // call real callback
    callback(raw_s);

  });

};

J.loader.prototype.cache_segmentation = function(x, y, z, w) {
  // now get some more images
  for (var j=1;j<=this._z_cache_size;j++) {
    if (z+j < this._viewer._image.max_z_tiles) {
      this.get_segmentation(x, y, z+j, w, function(s) {
      }, true);
    }
  }

};

J.loader.prototype.clear_cache_segmentation = function(x,y,z,w) {

  this._segmentation_cache[z] = [];
  // console.log('cache cleared.');

};

J.loader.prototype.load_tiles = function(x, y, z, w, w_new, no_draw) {

  var mojo_w_new = w_new;

  if (mojo_w_new < 0) {
    this._viewer.loading(false);
    return;
  }
  // TILESCOUNT FOR CURRENT ZOOMLEVEL IN X AND Y
  var tilescount_x = this._viewer._image.zoom_levels[mojo_w_new][0];
  var tilescount_y = this._viewer._image.zoom_levels[mojo_w_new][1];


  // I,J for the MOUSE (image space)
  var i_j = this._viewer._camera._i_j;
  if (i_j[0] == -1 || i_j[1] == -1) {
    i_j = [0,0];
  }

  // X, Y as tile indices for the MOUSE on highest resolution
  x = Math.floor(i_j[0] / 512);
  y = Math.floor(i_j[1] / 512);

  // now for the new zoomlevel
  x = Math.floor(x / Math.pow(2, w_new));
  y = Math.floor(y / Math.pow(2, w_new));

  var offset_x = this._viewer._camera._view[6];
  var offset_y = this._viewer._camera._view[7];

  var local_offset_x = (offset_x + x*(512 * this._viewer._camera._view[0]));
  var local_offset_y = (offset_y + y*(512 * this._viewer._camera._view[4]));

  var tiles_to_load = [];
  tiles_to_load.push([x,y]);

  // check how many surrounding tiles we should load
  var space_left = Math.max(0,local_offset_x);
  var space_top = Math.max(0,local_offset_y);
  var space_right = Math.max(0, this._viewer._width - (local_offset_x+512*this._viewer._camera._view[0]));
  var space_bottom = Math.max(0, this._viewer._height - (local_offset_y+512*this._viewer._camera._view[4]));

  var no_left = Math.ceil(space_left/(512*this._viewer._camera._view[0]));
  var no_top = Math.ceil(space_top/(512*this._viewer._camera._view[4]));
  var no_right = Math.ceil(space_right/(512*this._viewer._camera._view[0]));
  var no_bottom = Math.ceil(space_bottom/(512*this._viewer._camera._view[4]));

  for (var l=1; l<=no_left; l++) {
    var new_x = x-l;

    if (new_x < 0) break;
    tiles_to_load.push([new_x,y]);
  }

  for (var t=1; t<=no_top; t++) {
    var new_y = y-t;
    if (new_y < 0) break;
    tiles_to_load.push([x, new_y]);
  }

  for (var r=1; r<=no_right; r++) {
    var new_x = x+r;
    if (new_x >= tilescount_x) break;
    tiles_to_load.push([new_x, y]);
  }

  for (var b=1; b<=no_bottom; b++) {
    var new_y = y+b;
    if (new_y >= tilescount_y) break;
    tiles_to_load.push([x, new_y]);
  }


  for (var t=1; t<=no_top; t++) {
    var new_y = y-t;
    if (new_y < 0) break;
    for (var r=1; r<=no_right; r++) {
      var new_x = x+r;
      if (new_x >= tilescount_x) break;
      tiles_to_load.push([new_x, new_y]);
    }
  }

  for (var b=1; b<=no_bottom; b++) {
    var new_y = y+b;
    if (new_y >= tilescount_y) break;
    for (var r=1; r<=no_right; r++) {
      var new_x = x+r;
      if (new_x >= tilescount_x) break;
      tiles_to_load.push([new_x, new_y]);
    }
  }

  for (var t=1; t<=no_top; t++) {
    var new_y = y-t;
    if (new_y < 0) break;
    for (var l=1; l<=no_left; l++) {
      var new_x = x-l;

      if (new_x < 0) break;
      tiles_to_load.push([new_x,new_y]);
    }
  }

  for (var b=1; b<=no_bottom; b++) {
    var new_y = y+b;
    if (new_y >= tilescount_y) break;
    for (var l=1; l<=no_left; l++) {
      var new_x = x-l;

      if (new_x < 0) break;
      tiles_to_load.push([new_x,new_y]);
    }
  }

  // clear old tiles
  if (!no_draw) {
    this._viewer.clear_buffer(this._viewer._image.width, this._viewer._image.height);
  }

  var to_draw = tiles_to_load.length;
  var max_to_draw = tiles_to_load.length;
  for (var k=0; k<max_to_draw; k++) {

    var x_y = tiles_to_load[k];
    x = tiles_to_load[k][0];
    y = tiles_to_load[k][1];

    this.get_image(x, y, z, mojo_w_new, function(x, y, z, mojo_w_new, i) {

      this.get_segmentation(x, y, z, mojo_w_new, function(x, y, z, mojo_w_new, s) {

        if (!no_draw) this._viewer.draw_image(x, y, z, mojo_w_new, i, s);

        to_draw--;



        if (to_draw == 0) {

          this._viewer.loading(false);
        }

      }.bind(this, x, y, z, mojo_w_new));

    }.bind(this, x, y, z, mojo_w_new));

  }

};