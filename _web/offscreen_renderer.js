var J = J || {};

J.offscreen_renderer = function(viewer) {

  this._viewer = viewer;
  this._canvas = this._viewer._offscreen_buffer;
  this._controller = this._viewer._controller;

  this._gl = null;

  this._program = null;

  this._square_buffer = null;
  this._uv_buffer = null;

  this._width = this._canvas.width;
  this._height = this._canvas.height;

  this._merge_table_changed = true;

};

J.offscreen_renderer.prototype.init = function(vs_id, fs_id) {

  var canvas = this._canvas;
  var no_alias = {
    "antialias": false,
  }
  var gl = canvas.getContext('webgl2', no_alias);

  if (!gl) {
    return false;
  }

  gl.viewport(0, 0, this._width, this._height);
  gl.clearColor(0,0,0,1.);
  gl.clearDepth(0);

  // enable transparency
  gl.blendEquation(gl.FUNC_ADD);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  gl.enable(gl.BLEND);
  // Clear everything
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // create shaders
  this._program = linkShaders(gl, vs_id, fs_id);
  var h = this._program;
  if (!h) {
    return false;
  }
  gl.useProgram(h);

  // Get all uniform locations
  this._uni = {};
  var uniforms = [
    'uMergeTableKeySampler', 'uMergeTableValueSampler', 'uLockTableSampler',
    'uTextureSampler', 'uImageSampler', 'uColorMapSampler',
    'uSplitMode', 'uAdjustMode', 'uMaxColors', 'uBorders',
    'uOpacity', 'uHighlightedId', 'uActivatedId',
    'uMergeTableLength', 'uLockTableLength',
    'uOnlyLocked', 'uShowOverlay',
  ];
  uniforms.forEach(function(u){
    this._uni[u] = gl.getUniformLocation(h, u);
  }, this);

  // Get all attribute locations
  this._att = {};
  var attributes = ['aPosition', 'aTexturePosition'];
  attributes.forEach(function(a){
    this._att[a] = gl.getAttribLocation(h, a);
  }, this);

  this._tex = {
    'ids': {
      name: 'TEXTURE0',
      sampler: this._uni['uTextureSampler'],
    },
    'colormap': {
      name: 'TEXTURE1',
      sampler: this._uni['uColorMapSampler'],
    },
    'merge_keys': {
      name: 'TEXTURE2',
      sampler: this._uni['uMergeTableKeySampler'],
    },
    'merge_values': {
      name: 'TEXTURE3',
      sampler: this._uni['uMergeTableValueSampler'],
    },
    'lock_values': {
      name: 'TEXTURE4',
      sampler: this._uni['uLockTableSampler'],
    },
    'image': {
      filter: 'LINEAR',
      name: 'TEXTURE5',
      sampler: this._uni['uImageSampler'],
    },
  }

  // Vertex Position Buffer
  var vertexPos = new Float32Array([
      -1.0, -1.0,
       1.0, -1.0,
       1.0,  1.0,
       1.0,  1.0,
      -1.0,  1.0,
      -1.0, -1.0
  ]);
  this._vertexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, this._vertexBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertexPos, gl.STATIC_DRAW);
  gl.bindBuffer(gl.ARRAY_BUFFER, null);

  // Texture Position Buffer
  var texturePos = new Float32Array([
      0.0, 1.0,
      1.0, 1.0,
      1.0, 0.0,
      1.0, 0.0,
      0.0, 0.0,
      0.0, 1.0
  ]);
  this._textureBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, this._textureBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, texturePos, gl.STATIC_DRAW);
  gl.bindBuffer(gl.ARRAY_BUFFER, null);

  this._gl = gl;

  this.init_buffers();

  return true;

};

J.offscreen_renderer.prototype.init_buffers = function() {

  var gl = this._gl;

  // Set all texture paramters
  for ( tex in this._tex) {

    var vals = this._tex[tex];
    var filter = vals.filter || 'NEAREST';

    // Get texture location and order
    vals.texture = gl.createTexture();
    vals.id = Number(vals.name.match(/\d+/)[0]);

    // Set texture parameters one time
    gl.bindTexture(gl.TEXTURE_2D, vals.texture);

    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl[filter]);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl[filter]);

    gl.bindTexture(gl.TEXTURE_2D, null);
  }

};

J.offscreen_renderer.prototype.draw = function(i, s, c, x, y) {

  var gl = this._gl;

  gl.viewport(0, 0, this._width, this._height);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);


  if (this._controller._gl_colormap_changed) {

    // update colormap texture buffer
    gl.bindTexture(gl.TEXTURE_2D, this._tex.colormap.texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, this._viewer._max_colors, 1, 0, gl.RGB, gl.UNSIGNED_BYTE, this._viewer._gl_colormap);

    this._controller._gl_colormap_changed = false;

  }

  // create segmentation texture buffer
  gl.bindTexture(gl.TEXTURE_2D, this._tex.ids.texture);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8UI, 512, 512, 0, gl.RGBA_INTEGER, gl.UNSIGNED_BYTE, s);


  // create image texture buffer
  gl.bindTexture(gl.TEXTURE_2D, this._tex.image.texture);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, i);


  //
  // MERGE TABLE
  //
  var merge_table_length = this._controller._merge_table_length;

  if (this._controller._gl_merge_table_changed) {

    gl.bindTexture(gl.TEXTURE_2D, this._tex.merge_keys.texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8UI, merge_table_length, 1, 0, gl.RGBA_INTEGER, gl.UNSIGNED_BYTE, this._controller._gl_merge_table_keys);

    gl.bindTexture(gl.TEXTURE_2D, this._tex.merge_values.texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8UI, merge_table_length, 1, 0, gl.RGBA_INTEGER, gl.UNSIGNED_BYTE, this._controller._gl_merge_table_values);

    this._controller._gl_merge_table_changed = false;

  }

  //
  // LOCK TABLE
  //
  var lock_table_length = this._controller._lock_table_length;

  if (this._controller._gl_lock_table_changed) {

    gl.bindTexture(gl.TEXTURE_2D, this._tex.lock_values.texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8UI, lock_table_length, 1, 0, gl.RGBA_INTEGER, gl.UNSIGNED_BYTE, this._controller._gl_lock_table);

    this._controller._gl_lock_table_changed = false;

  }

  // Values for given IDs
  gl.uniform1ui(this._uni.uActivatedId, this._viewer._controller._activated_id);
  gl.uniform1ui(this._uni.uHighlightedId, this._viewer._controller._highlighted_id);

  // Display settings
  gl.uniform1i(this._uni.uShowOverlay, this._viewer._overlay_show);
  gl.uniform1f(this._uni.uOpacity, this._viewer._overlay_opacity);
  gl.uniform1i(this._uni.uBorders, this._viewer._overlay_borders);
  gl.uniform1i(this._uni.uOnlyLocked, this._viewer._only_locked);

  // Flags for current modes
  gl.uniform1i(this._uni.uSplitMode, this._viewer._controller._split_mode);
  gl.uniform1i(this._uni.uAdjustMode, this._viewer._controller._adjust_mode);

  // Information about textures
  gl.uniform1f(this._uni.uLockTableLength, lock_table_length);
  gl.uniform1f(this._uni.uMaxColors, this._viewer._max_colors);
  gl.uniform1f(this._uni.uMergeTableLength, merge_table_length);

  // Bind the Vertex Buffer
  gl.enableVertexAttribArray(this._att.aPosition);
  gl.bindBuffer(gl.ARRAY_BUFFER, this._vertexBuffer);
  gl.vertexAttribPointer(this._att.aPosition, 2, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ARRAY_BUFFER, null);

  // Bind the Texture Buffer
  gl.enableVertexAttribArray(this._att.aTexturePosition);
  gl.bindBuffer(gl.ARRAY_BUFFER, this._textureBuffer);

  // ↓タイプミスを修正。undefinedのまま関数に渡され、関数も文句いわずにno-opしちゃうので直す
  //gl.vertexAttribPointer(this._att.TexturePosition, 2, gl.FLOAT, false, 0, 0);
  gl.vertexAttribPointer(this._att.aTexturePosition, 2, gl.FLOAT, false, 0, 0);

  gl.bindBuffer(gl.ARRAY_BUFFER, null);

  // Add all the textures to the shaders
  for (tex in this._tex) {

    var vals = this._tex[tex];
    gl.activeTexture(gl[vals.name]);
    gl.bindTexture(gl.TEXTURE_2D, vals.texture);
    gl.uniform1i(vals.sampler, vals.id);
  }

  // 黒いloadingのままになってしまうのを修正
  // gl.drawArrays(gl.TRIANGLES, 0, 6); <==================================
  gl.drawArrays(gl.TRIANGLES, 0, 6);


  c.drawImage(this._canvas,0,0,512,512,x*512,y*512,512,512);

};
