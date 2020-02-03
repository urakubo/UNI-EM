/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return DOJO_CANVAS_BUFFER_WIDTH; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return DOJO_CANVAS_BUFFER_HEIGHT; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "h", function() { return SLICE_SLIDER_MIN_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "i", function() { return SLICE_SLIDER_STEP; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "g", function() { return SLICE_SLIDER_DEFAULT_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "e", function() { return OPACITY_SLIDER_MIN_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "d", function() { return OPACITY_SLIDER_MAX_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "f", function() { return OPACITY_SLIDER_STEP; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "c", function() { return OPACITY_SLIDER_DEFAULT_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "l", function() { return ZOOM_SLIDER_MIN_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "k", function() { return ZOOM_SLIDER_MAX_VALUE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "m", function() { return ZOOM_SLIDER_STEP; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "j", function() { return ZOOM_SLIDER_DEFAULT_VALUE; });
// 共通設定

/**
 * canvasの幅と高さ
 *
 * 定義元:
 *   _web/viewer.js
 *     this._segmentation_buffer.width
 *     this._segmentation_buffer.height
 *     this._offscreen_buffer.width
 *     this._offscreen_buffer.height
 *     他、直接ソース上に512と記述されてるところ
 */

// canvasの幅
var DOJO_CANVAS_BUFFER_WIDTH = 512;

// canvasの高さ
var DOJO_CANVAS_BUFFER_HEIGHT = 512;

/**
 * slice
 *
 * コマンド:
 *   87: W SLICE UP
 *   83: S SLICE DOWN
 *
 * 定義元:
 *   _web/camera.js
 *     J.camera.prototype.slice_up
 *     J.camera.prototype.slice_down
 *
 *   _web/dojo.js
 *     DOJO.update_slice_number
 */

// sliceスライダーの最小値
// 最大値はdojoの読み込みが完了したときのイベント_onDojoImageLoadCompleteで設定する
var SLICE_SLIDER_MIN_VALUE = 1;

// sliceスライダーを動かすといくつ動くか
var SLICE_SLIDER_STEP = 1;

// sliceスライダーの初期値
var SLICE_SLIDER_DEFAULT_VALUE = 1;

/**
 * opacity
 *
 * コマンド:
 *   189: - DECREASE OPACITY
 *   187: = INCREASE OPACITY
 *
 * 定義元:
 *   _web/viewer.js
 *     J.viewer.prototype.increase_opacity
 *     J.viewer.prototype.decrease_opacity
 *     this._overlay_opacity
 */

// opacityスライダーの最小値
var OPACITY_SLIDER_MIN_VALUE = 0;

// opacityスライダーの最大値
var OPACITY_SLIDER_MAX_VALUE = 255;

// opacityスライダーを動かすといくつ動くか
var OPACITY_SLIDER_STEP = 20;

// opacityスライダーの初期値
var OPACITY_SLIDER_DEFAULT_VALUE = 100;

/**
 * zoom
 *
 * コマンド:
 *   67: C ZOOM IN
 *   88: X ZOOM OUT
 *
 * 定義元:
 *   _web/camera.js
 *     J.camera.prototype.zoom
 */

// zoomスライダーの最小値
var ZOOM_SLIDER_MIN_VALUE = 1;

// zoomスライダーの最大値
// 本来camera.jsのfuture_zoom_levelを使うが、バグがあるため
// 初期状態から何回ズームできるかを単純に数えた数
var ZOOM_SLIDER_MAX_VALUE = 13;

// zoomスライダーを動かすといくつ動くか
var ZOOM_SLIDER_STEP = 1;

// zoomスライダーの初期値
var ZOOM_SLIDER_DEFAULT_VALUE = 2;

/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export triggerKeydown */
/* harmony export (immutable) */ __webpack_exports__["a"] = addAfter;
/* harmony export (immutable) */ __webpack_exports__["c"] = getWindowCenterPos;
/* harmony export (immutable) */ __webpack_exports__["b"] = getCameraCenterPos;
/* harmony export (immutable) */ __webpack_exports__["d"] = isOverImage;
/* harmony export (immutable) */ __webpack_exports__["e"] = isZoomableImage;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__config__ = __webpack_require__(0);
// 汎用ユーティリティなど



/**
 * keydownイベントを発火する
 *
 * @param  {number} keyCode 発火するキーコード
 */
function triggerKeydown(keyCode) {
  var event = $.Event('keydown');
  event.keyCode = keyCode;
  $(window).trigger(event);
}

/**
 * メソッドが呼ばれた後に任意の処理を追加する
 *
 * @param {Object} target 対象のオブジェクト
 * @param {string} name 対象のメソッド名
 * @param {Function} before 後に追加する処理
 *                          オリジナルの引数が全て渡されて呼び出される
 * @return 元のメソッドの戻り値が返る
 */
function addAfter(target, name, after) {
  var original = target[name];
  target[name] = function () {
    var result = original.apply(this, arguments);
    after.apply(this, arguments);
    return result;
  };
}

/**
 * windowの中央位置を取得する
 *
 * @return {Object} 位置が定義されたオブジェクト
 *   - x : 画面の横軸中央
 *   - y : 画面の縦軸中央
 */
function getWindowCenterPos() {
  var x = Math.floor($(window).width() / 2);
  var y = Math.floor($(window).height() / 2);

  return {
    x: x,
    y: y
  };
}

/**
 * dojoのcamera(メインのcanvas)の中央位置を取得する
 *
 * 参考:
 *   _web/camera.js
 *     J.camera.prototype.center
 *
 * @return {Object} 位置が定義されたオブジェクト
 *   - x      : 画面の横軸中央
 *   - y      : 画面の縦軸中央
 *   - left   : cameraの左位置
 *   - right  : cameraの右位置
 *   - top    : cameraの上位置
 *   - bottom : cameraの下位置
 */
function getCameraCenterPos() {
  var centerX = DOJO.viewer._width / 2;
  var centerY = DOJO.viewer._height / 2;

  var canvasLeft = centerX - __WEBPACK_IMPORTED_MODULE_0__config__["b" /* DOJO_CANVAS_BUFFER_WIDTH */] / 2;
  var canvasRight = canvasLeft + __WEBPACK_IMPORTED_MODULE_0__config__["b" /* DOJO_CANVAS_BUFFER_WIDTH */];
  var canvasTop = centerY - __WEBPACK_IMPORTED_MODULE_0__config__["a" /* DOJO_CANVAS_BUFFER_HEIGHT */] / 2;
  var canvasBottom = canvasTop + __WEBPACK_IMPORTED_MODULE_0__config__["a" /* DOJO_CANVAS_BUFFER_HEIGHT */];

  return {
    x: centerX,
    y: centerY,
    left: canvasLeft,
    right: canvasRight,
    top: canvasTop,
    bottom: canvasBottom
  };
}

/**
 * 指定の座標がcanvasのイメージ上にあるかどうか
 *
 * @param  {number}  x x座標
 * @param  {number}  y y座標
 * @return {Boolean}
 */
function isOverImage(x, y) {
  var u_v = DOJO.viewer.xy2uv(x, y);
  return u_v[0] !== -1 && u_v[1] !== -1;
}

/**
 * 正しくズームできるかどうか
 * 読み込んだ画像が正方形じゃなかった場合、余った領域は黒くなる
 * その黒い部分はマウスカーソルが反応しないためズームができない
 *
 * @param  {number} canvasImageWidth  読み込んだイメージのwidth
 * @param  {number} canvasImageHeight 読み込んだイメージのheight
 * @return {Boolean}
 */
function isZoomableImage(canvasImageWidth, canvasImageHeight) {
  var half = canvasImageHeight / 2;
  return canvasImageWidth - half > 0;
}

/***/ }),
/* 2 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return BaseSlider; });
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * sliderの基底クラス
 */
var BaseSlider = function () {
  _createClass(BaseSlider, [{
    key: 'template',
    get: function get() {
      return _.template('<input type="text">');
    }
  }]);

  function BaseSlider() {
    _classCallCheck(this, BaseSlider);

    this.el = null;
    this.wrapperEl = null;
    this.sliderMin = null;
    this.sliderMax = null;
    this.sliderStep = null;
    this.sliderValue = null;
    this.sliderOptions = null;
    this.isSliderReady = false;
    this.initialized = false;
  }

  _createClass(BaseSlider, [{
    key: 'initSlider',
    value: function initSlider() {
      var _this = this;

      if (this.initialized) {
        return;
      }
      this.initialized = true;

      this.el = $(this.template());
      this.wrapperEl.append(this.el);

      var sliderOptions = Object.assign({}, {
        min: this.sliderMin,
        max: this.sliderMax,
        step: this.sliderStep,
        value: this.sliderValue,
        formatter: function formatter() {
          return _this.sliderFormatter.apply(_this, arguments);
        }
      }, this.sliderOptions || {});

      this.el.bootstrapSlider(sliderOptions).on('change', function () {
        _this.onSliderChange.apply(_this, arguments);
      });
    }
  }, {
    key: 'sliderFormatter',
    value: function sliderFormatter(value) {
      return value + '/' + this.sliderMax;
    }
  }, {
    key: 'onSliderChange',
    value: function onSliderChange(event) {}
  }, {
    key: 'getValue',
    value: function getValue() {
      return this.el.bootstrapSlider('getValue');
    }
  }, {
    key: 'setValue',
    value: function setValue(value) {
      return this.el.bootstrapSlider('setValue', value);
    }
  }]);

  return BaseSlider;
}();

/***/ }),
/* 3 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__dojo_extension__ = __webpack_require__(4);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__dojo_gui__ = __webpack_require__(5);



(function () {
  if (window.DojoGUI) {
    return;
  }

  Object(__WEBPACK_IMPORTED_MODULE_0__dojo_extension__["a" /* extendDojo */])();
  window.DojoGUI = new __WEBPACK_IMPORTED_MODULE_1__dojo_gui__["a" /* DojoGUI */]();
})();

/***/ }),
/* 4 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["a"] = extendDojo;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__util__ = __webpack_require__(1);


// GUI化するために必要なdojoの機能拡張

var extended = false;

function extendDojo() {
  if (extended) {
    return;
  }
  extended = true;

  /**
   * Loading用拡張
   */

  // Loading開始/完了時にフック用イベントを追加する
  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.viewer.prototype, 'loading', function () {
    var isReady = this._image_buffer_ready;
    EventBus.dispatch('DOJO:loading', null, isReady);
  });

  /**
   * Slice用拡張
   */

  // sliceのスライダーでシークするときにnext(+1), prev(-1)以外に特定の値にシークする場合
  // dojoの機能では用意されていないので拡張する
  Object.assign(J.camera.prototype, {

    /**
     * slice_number(n)に移動する
     *
     * _web/camera.js
     *     J.camera.prototype.slice_up
     *     J.camera.prototype.slice_down
     * とほぼ同じことをする
     *
     * @param {number} n シークする番号
     */
    slice_seek: function slice_seek(n) {
      if (this._z < 0) {
        return;
      }
      if (this._z > this._viewer._image.max_z_tiles - 1) {
        return;
      }

      if (this._viewer._controller._split_mode != -1 && this._viewer._controller._split_mode != 666) {
        return;
      }
      if (this._viewer._controller._adjust_mode != -1 && !DOJO.single_segment) {
        return;
      }

      this._viewer._controller.clear_exclamationmarks();
      this._viewer._controller.reset_cursors();

      this._viewer.loading(true);
      var oldZ = this._z;
      this._z = n - 1;

      this._loader.load_tiles(this._x, this._y, this._z, this._w, this._w, false);

      if (DOJO.threeD) {
        // 3D Viewerを表示してるときの赤い線を移動する
        var count = this._z - oldZ;
        if (this._z > oldZ) {
          while (--count >= 0) {
            DOJO.threeD.slice.transform.translateZ(DOJO.threeD.volume.spacing[2] * this._zStack);
          }
        } else {
          count = Math.abs(count);
          while (--count >= 0) {
            DOJO.threeD.slice.transform.translateZ(-DOJO.threeD.volume.spacing[2] * this._zStack);
          }
        }
      }

      DOJO.update_slice_number(this._z + 1);
    }
  });

  // DOJO.update_slice_number が呼ばれた後にイベントを発行する
  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](DOJO, 'update_slice_number', function (n) {
    EventBus.dispatch('DOJO:sliceNumberChange', null, n, DOJO.viewer._image.max_z_tiles);
  });

  /**
   * Opacity用拡張
   */

  // opacityのスライダーでシークするときにincrease opacity(+1), decrease opacity (-1)以外に特定の値にシークする場合
  // dojoの機能では用意されていないので拡張する
  Object.assign(J.viewer.prototype, {

    /**
     * opacityをnに設定する
     *
     *  _web/viewer.js
     *     J.viewer.prototype.increase_opacity
     *     J.viewer.prototype.decrease_opacity
     *  とほぼ同じことをする
     *
     * @param {number} n 設定するopacityの値
     */
    set_opacity: function set_opacity(n) {
      this._overlay_opacity = Math.min(255, Math.max(0, n));
      this.redraw();
    }
  });

  // opacityが変わった後にイベントを発行する
  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.viewer.prototype, 'increase_opacity', function () {
    EventBus.dispatch('DOJO:opacityChange', null, this._overlay_opacity);
  });

  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.viewer.prototype, 'decrease_opacity', function () {
    EventBus.dispatch('DOJO:opacityChange', null, this._overlay_opacity);
  });

  /**
   * Zoom用拡張
   */

  Object.assign(J.camera.prototype, {
    // J.camera.prototype.centerと同じ処理
    fix_center: function fix_center() {
      var diff = this._viewer._image.width - this._viewer._image.height / 2;
      if (diff > 0) {
        diff = 0;
      } else {
        // 1pxずらして中央位置の基点をずらし、ズームできるようにする
        diff--;
      }
      this._view[6] = this._viewer._width / 2 - 512 / 2 - diff;
      this._view[7] = this._viewer._height / 2 - 512 / 2;
    }
  });

  // zoom時にスライダーと動きを連動させるためにフック用イベントを追加する
  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.camera.prototype, 'zoom', function (x, y, delta) {
    var u_v = this._viewer.xy2uv(x, y);
    // マウスカーソルがcanvas上じゃなかった場合は実際にズームされないのでスキップ
    if (u_v[0] == -1 || u_v[1] == -1) {
      return;
    }

    // zoomレベルの取得方法、違う可能性あり
    // this._view[4]で合ってるか?
    // 3回くらい拡大すると一旦future_zoom_levelがリセットされてしまうため値がおかしくなる
    // dojo側のバグ?
    var future_zoom_level = this._view[4];
    EventBus.dispatch('DOJO:zoomChange', null, x, y, delta, future_zoom_level);
  });

  /**
   * Marge, Split Modeに切り替わったとき、オフになったときにフック用イベントを追加する
   */
  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](DOJO, 'reset_tools', function () {
    EventBus.dispatch('DOJO:resetTools', null);
  });

  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.controller.prototype, 'merge', function (id) {
    EventBus.dispatch('DOJO:merge', null, id);
  });

  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.controller.prototype, 'start_split', function (id, x, y) {
    EventBus.dispatch('DOJO:startSplit', null, id, x, y);
  });

  /**
   * その他の拡張
   */

  // 読み込み時/読み込み完了にフック用イベントを追加する
  __WEBPACK_IMPORTED_MODULE_0__util__["a" /* addAfter */](J.viewer.prototype, 'loading', function (value) {
    if (this._image_buffer_ready) {
      EventBus.dispatch('DOJO:imageLoadComplete', null, this);
    } else {
      EventBus.dispatch('DOJO:imageLoadStart', null, this);
    }
  });
}

/***/ }),
/* 5 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return DojoGUI; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__header_toolbar__ = __webpack_require__(6);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__slice_slider__ = __webpack_require__(7);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__opacity_slider__ = __webpack_require__(8);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__zoom_slider__ = __webpack_require__(9);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }






var DojoGUI = function () {
  function DojoGUI() {
    _classCallCheck(this, DojoGUI);

    this._elementsInitialized = false;
  }

  _createClass(DojoGUI, [{
    key: 'init',
    value: function init() {
      var _this = this;

      EventBus.addEventListener('DOJO:loading', function () {
        return _this.onDojoLoading.apply(_this, arguments);
      });
      EventBus.addEventListener('DOJO:merge', function () {
        return _this.onDojoMerge.apply(_this, arguments);
      });
      EventBus.addEventListener('DOJO:startSplit', function () {
        return _this.onDojoStartSplit.apply(_this, arguments);
      });
      EventBus.addEventListener('DOJO:resetTools', function () {
        return _this.onDojoResetTools.apply(_this, arguments);
      });
    }
  }, {
    key: 'onDojoLoading',
    value: function onDojoLoading(event, isReady) {
      if (isReady && !this._elementsInitialized) {
        this._elementsInitialized = true;
        this.initElements();
      }
    }
  }, {
    key: 'initElements',
    value: function initElements() {
      this.headerToolbar = new __WEBPACK_IMPORTED_MODULE_0__header_toolbar__["a" /* HeaderToolbar */]();
      this.sliceSlider = new __WEBPACK_IMPORTED_MODULE_1__slice_slider__["a" /* SliceSlider */]();
      this.opacitySlider = new __WEBPACK_IMPORTED_MODULE_2__opacity_slider__["a" /* OpacitySlider */]();
      this.zoomSlider = new __WEBPACK_IMPORTED_MODULE_3__zoom_slider__["a" /* ZoomSlider */]();
    }

    /**
     * camera用のスライダーを有効化
     */

  }, {
    key: 'enableCameraSliders',
    value: function enableCameraSliders() {
      this.sliceSlider.el.bootstrapSlider('enable');
      this.zoomSlider.el.bootstrapSlider('enable');
    }

    /**
     * camera用のスライダーを無効化
     */

  }, {
    key: 'disableCameraSliders',
    value: function disableCameraSliders() {
      this.sliceSlider.el.bootstrapSlider('disable');
      this.zoomSlider.el.bootstrapSlider('disable');
    }

    /**
     * Margeモードに切り替わった時のイベント
     *
     * @param  {Object} event イベントオブジェクト
     * @param  {number} id    merge時に渡されるパラメータ
     */

  }, {
    key: 'onDojoMerge',
    value: function onDojoMerge(event, id) {
      this.disableCameraSliders();
    }

    /**
     * Splitモードに切り替わった時のイベント
     *
     * @param  {Object} event イベントオブジェクト
     * @param  {number} id    split時に渡されるパラメータ
     * @param  {number} x     split時に渡されるパラメータ
     * @param  {number} y     split時に渡されるパラメータ
     */

  }, {
    key: 'onDojoStartSplit',
    value: function onDojoStartSplit(event, id, x, y) {
      this.disableCameraSliders();
    }

    /**
     * DOJO.reset_toolsが実行された時のイベント
     *
     * @param  {Object} event イベントオブジェクト
     */

  }, {
    key: 'onDojoResetTools',
    value: function onDojoResetTools() {
      this.enableCameraSliders();
    }
  }]);

  return DojoGUI;
}();

/***/ }),
/* 6 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return HeaderToolbar; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__config__ = __webpack_require__(0);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }



var HeaderToolbar = function () {
  function HeaderToolbar() {
    var _this = this;

    _classCallCheck(this, HeaderToolbar);

    this.el = $('.gui-header-toolbar');
    this.infopanel = $('.infopanel');

    this.menu = this.el.find('.gui-menu');
    this.menu.on('click', function () {
      return _this.onMenuClick.apply(_this, arguments);
    });

    this.menuLabel = this.menu.find('.gui-menu-label');
  }

  _createClass(HeaderToolbar, [{
    key: 'onMenuClick',
    value: function onMenuClick(event) {
      var _this2 = this;

      return new Promise(function (resolve, reject) {
        _this2.infopanel.slideToggle('fast').promise().done(function () {
          if (_this2.infopanel.is(':visible')) {
            _this2.menuLabel.text('Close Menu');
          } else {
            _this2.menuLabel.text('Open Menu');
          }
        });
      });
    }
  }]);

  return HeaderToolbar;
}();

/***/ }),
/* 7 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SliceSlider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__base_slider__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__config__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__util__ = __webpack_require__(1);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }





var SliceSlider = function (_BaseSlider) {
  _inherits(SliceSlider, _BaseSlider);

  function SliceSlider() {
    _classCallCheck(this, SliceSlider);

    var _this = _possibleConstructorReturn(this, (SliceSlider.__proto__ || Object.getPrototypeOf(SliceSlider)).call(this));

    _this._targetSliceNumber = null;
    _this._isSeeking = false;
    _this._seekQueue = [];

    _this.sliderMin = __WEBPACK_IMPORTED_MODULE_1__config__["h" /* SLICE_SLIDER_MIN_VALUE */];
    _this.sliderStep = __WEBPACK_IMPORTED_MODULE_1__config__["i" /* SLICE_SLIDER_STEP */];
    _this.sliderValue = __WEBPACK_IMPORTED_MODULE_1__config__["g" /* SLICE_SLIDER_DEFAULT_VALUE */];

    _this.wrapperEl = $('.gui-slice-wrapper');
    _this.sliderOptions = {};

    EventBus.addEventListener('DOJO:sliceNumberChange', function () {
      _this._onDojoSliceNumberChange.apply(_this, arguments);
    });
    EventBus.addEventListener('DOJO:imageLoadComplete', function () {
      _this._onDojoImageLoadComplete.apply(_this, arguments);
    });
    return _this;
  }

  _createClass(SliceSlider, [{
    key: 'sliderFormatter',
    value: function sliderFormatter(value) {
      // DOJO.update_slice_numberに合わせて-1の値にする
      return value - 1 + '/' + (this.sliderMax - 1);
    }

    /**
     * スライダーをcameraと同じ位置に置く
     */

  }, {
    key: 'setWrapperPositon',
    value: function setWrapperPositon() {
      var _util$getCameraCenter = __WEBPACK_IMPORTED_MODULE_2__util__["b" /* getCameraCenterPos */](),
          left = _util$getCameraCenter.left,
          bottom = _util$getCameraCenter.bottom;

      // 横位置をcameraと同じに揃える


      var wrapperLeft = left;
      // 縦位置をcameraのすぐ下に揃える
      var wrapperTop = bottom + 20;

      // スライダーを表示する
      this.wrapperEl.css({
        left: wrapperLeft,
        top: wrapperTop
      }).show();
    }
  }, {
    key: 'isSlicing',
    value: function isSlicing() {
      return this._targetSliceNumber != null;
    }
  }, {
    key: 'sliceSeek',
    value: function sliceSeek(value) {
      var _this2 = this;

      return new Promise(function (resolve, reject) {
        _this2._targetSliceNumber = value;
        DOJO.viewer._camera.slice_seek(value);

        // dojo本体のslice numberが更新されるまで待機する
        chillout.till(function () {
          if (!_this2.isSlicing()) {
            return false; // stop iteration
          }
        }).then(function () {
          resolve();
        });
      });
    }
  }, {
    key: 'onSliderChange',
    value: function onSliderChange(event) {
      var _this3 = this;

      var _event$value = event.value,
          oldValue = _event$value.oldValue,
          newValue = _event$value.newValue;

      // スライス途中だったら無視する

      if (this.isSlicing()) {
        event.preventDefault();
        this.setValue(oldValue);
        return;
      }

      // 動かしてる途中だったら処理が重ならないようにする
      var seek = function seek() {
        _this3._isSeeking = true;
        _this3.sliceSeek(newValue).then(function () {
          if (_this3._seekQueue.length > 0) {
            // シークのつまみを早く動かした場合、つまみを動かした分すべて実行するとカクカクと重くなるので
            // 不要な処理を除外する。最後の動きだけがあれば十分と思われる
            // 2コマ以上あったら捨てていく
            while (_this3._seekQueue.length > 2) {
              _this3._seekQueue.shift();
            }

            var queue = _this3._seekQueue.shift();
            queue();
          }
          _this3._isSeeking = false;
        });
      };

      if (this._isSeeking) {
        this._seekQueue.push(seek);
        return;
      }
      seek();
    }

    /**
     * dojoのupdate_slice_numberが呼ばれたときのイベント
     *
     * @param  {Object} event イベントオブジェクト
     * @param  {number} n 現在のslice number
     * @param  {number} maxZTiles slice numberとしての最大値
     */

  }, {
    key: '_onDojoSliceNumberChange',
    value: function _onDojoSliceNumberChange(event, n, maxZTiles) {
      if (!this.isSliderReady) {
        return;
      }

      if (this.isSlicing()) {
        if (this._targetSliceNumber === n) {
          // dojo本体のslice numberが更新された
          this._targetSliceNumber = null;
        }
        return;
      }

      var value = this.getValue();
      if (value !== n) {
        this.setValue(n);
      }
    }

    /**
     * dojoの読み込みが完了したときのイベント
     *
     * @param {Object} event イベントオブジェクト
     * @param {Object} viewer dojoのviewerインスタンス
     */

  }, {
    key: '_onDojoImageLoadComplete',
    value: function _onDojoImageLoadComplete(event, viewer) {
      if (!this.isSliderReady) {
        // スライダーの最大値を読み込んだイメージから取得する
        this.sliderMax = DOJO.viewer._image.max_z_tiles;
        this.initSlider();
        this.setWrapperPositon();
        this.isSliderReady = true;
      }
    }
  }]);

  return SliceSlider;
}(__WEBPACK_IMPORTED_MODULE_0__base_slider__["a" /* BaseSlider */]);

/***/ }),
/* 8 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return OpacitySlider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__base_slider__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__config__ = __webpack_require__(0);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }




var OpacitySlider = function (_BaseSlider) {
  _inherits(OpacitySlider, _BaseSlider);

  function OpacitySlider() {
    _classCallCheck(this, OpacitySlider);

    var _this = _possibleConstructorReturn(this, (OpacitySlider.__proto__ || Object.getPrototypeOf(OpacitySlider)).call(this));

    _this.sliderMin = __WEBPACK_IMPORTED_MODULE_1__config__["e" /* OPACITY_SLIDER_MIN_VALUE */];
    _this.sliderMax = __WEBPACK_IMPORTED_MODULE_1__config__["d" /* OPACITY_SLIDER_MAX_VALUE */];
    _this.sliderStep = __WEBPACK_IMPORTED_MODULE_1__config__["f" /* OPACITY_SLIDER_STEP */];
    _this.sliderValue = __WEBPACK_IMPORTED_MODULE_1__config__["c" /* OPACITY_SLIDER_DEFAULT_VALUE */];

    _this.wrapperEl = $('.gui-opacity-wrapper');
    _this.sliderOptions = {
      tooltip_position: 'bottom'
    };
    _this.initSlider();

    EventBus.addEventListener('DOJO:opacityChange', function () {
      _this._onDojoOpacityChange.apply(_this, arguments);
    });
    _this.isSliderReady = true;
    return _this;
  }

  _createClass(OpacitySlider, [{
    key: 'setOpacity',
    value: function setOpacity(opacity) {
      DOJO.viewer.set_opacity(opacity);
    }
  }, {
    key: 'onSliderChange',
    value: function onSliderChange(event) {
      var _event$value = event.value,
          oldValue = _event$value.oldValue,
          newValue = _event$value.newValue;

      this.setOpacity(newValue);
    }

    /**
     * dojoのopacityが変わったときのイベント
     *
     * @param {Object} event イベントオブジェクト
     * @param {number} opacity 不透明度
     */

  }, {
    key: '_onDojoOpacityChange',
    value: function _onDojoOpacityChange(event, opacity) {
      if (!this.isSliderReady) {
        return;
      }

      var value = this.getValue();
      if (value !== opacity) {
        this.setValue(opacity);
      }
    }
  }]);

  return OpacitySlider;
}(__WEBPACK_IMPORTED_MODULE_0__base_slider__["a" /* BaseSlider */]);

/***/ }),
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ZoomSlider; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__base_slider__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__config__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__util__ = __webpack_require__(1);
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }





var ZoomSlider = function (_BaseSlider) {
  _inherits(ZoomSlider, _BaseSlider);

  function ZoomSlider() {
    _classCallCheck(this, ZoomSlider);

    var _this = _possibleConstructorReturn(this, (ZoomSlider.__proto__ || Object.getPrototypeOf(ZoomSlider)).call(this));

    _this._zoomBySlider = false;

    // dojoのzoomで設定されるべきfuture_zoom_levelの値にバグ?があるため
    // このクラス内でzoom回数をレベルとしてカウントする
    _this._dojoZoomLevel = 1;

    _this.sliderMin = __WEBPACK_IMPORTED_MODULE_1__config__["l" /* ZOOM_SLIDER_MIN_VALUE */];
    _this.sliderMax = __WEBPACK_IMPORTED_MODULE_1__config__["k" /* ZOOM_SLIDER_MAX_VALUE */];
    _this.sliderStep = __WEBPACK_IMPORTED_MODULE_1__config__["m" /* ZOOM_SLIDER_STEP */];
    _this.sliderValue = __WEBPACK_IMPORTED_MODULE_1__config__["j" /* ZOOM_SLIDER_DEFAULT_VALUE */];

    _this.wrapperEl = $('.gui-zoom-wrapper');
    _this.sliderOptions = {
      precision: 1,
      tooltip: 'hide',
      tooltip_position: 'bottom'
    };
    _this.initSlider();

    EventBus.addEventListener('DOJO:zoomChange', function () {
      _this._onDojoZoomChange.apply(_this, arguments);
    });
    EventBus.addEventListener('DOJO:imageLoadComplete', function () {
      _this._onDojoImageLoadComplete.apply(_this, arguments);
    });
    return _this;
  }

  _createClass(ZoomSlider, [{
    key: 'sliderFormatter',
    value: function sliderFormatter(value) {
      return '';
    }
  }, {
    key: 'zoomIn',
    value: function zoomIn() {
      this.setZoom(1);
    }
  }, {
    key: 'zoomOut',
    value: function zoomOut() {
      this.setZoom(-1);
    }

    /**
     * delta値を指定してzoomする
     *
     * 参考:
     *   _web/interactor.js
     *     J.interactor.prototype.onmousewheel
     *
     * @param {number} delta zoomの基準となるdelta値
     */

  }, {
    key: 'setZoom',
    value: function setZoom(delta) {
      var _util$getWindowCenter = __WEBPACK_IMPORTED_MODULE_2__util__["c" /* getWindowCenterPos */](),
          x = _util$getWindowCenter.x,
          y = _util$getWindowCenter.y;

      DOJO.viewer._camera._x = x;
      DOJO.viewer._camera._y = y;
      DOJO.viewer._camera._i_j = DOJO.viewer.xy2ij(x, y);
      DOJO.viewer._camera.zoom(x, y, delta);
    }
  }, {
    key: 'onSliderChange',
    value: function onSliderChange(event) {
      var _event$value = event.value,
          oldValue = _event$value.oldValue,
          newValue = _event$value.newValue;


      this._zoomBySlider = true;

      // 正しくズームされないのを対処
      if (this.fixCenterPos()) {
        event.preventDefault();
        return;
      }

      if (oldValue < newValue) {
        this.zoomIn();
      } else if (oldValue > newValue) {
        this.zoomOut();
      }
    }

    /**
     * moveで移動してる場合、正しくズームされないので初期位置に戻す
     *
     * @return {Boolean} 初期位置に戻した場合trueが返る
     */

  }, {
    key: 'fixCenterPos',
    value: function fixCenterPos() {
      var _util$getWindowCenter2 = __WEBPACK_IMPORTED_MODULE_2__util__["c" /* getWindowCenterPos */](),
          x = _util$getWindowCenter2.x,
          y = _util$getWindowCenter2.y;

      if (!__WEBPACK_IMPORTED_MODULE_2__util__["d" /* isOverImage */](x, y)) {
        DOJO.viewer._camera.fix_center();
        if (this.getValue() !== this.sliderMin) {
          this.setValue(this.sliderMin);
        }
        return true;
      }

      return false;
    }

    /**
     * dojoのzoomが変わったときのイベント
     *
     * @param {Object} event イベントオブジェクト
     * @param {number} x マウスカーソルのx座標
     * @param {number} x マウスカーソルのy座標
     * @param {number} delta 拡大の基準値
     * @param {number} future_zoom_level 新しい拡大値
     */

  }, {
    key: '_onDojoZoomChange',
    value: function _onDojoZoomChange(event, x, y, delta, future_zoom_level) {
      if (!this.isSliderReady) {
        return;
      }

      if (this._zoomBySlider) {
        this._zoomBySlider = false;
        return;
      }

      if (delta > 0) {
        this._dojoZoomLevel++;
        if (this._dojoZoomLevel > this.sliderMax) {
          this._dojoZoomLevel = this.sliderMax;
        }
      } else if (delta < 0) {
        this._dojoZoomLevel--;
        if (this._dojoZoomLevel < this.sliderMin) {
          this._dojoZoomLevel = this.sliderMin;
        }
      }

      var value = this.getValue();
      if (value !== this._dojoZoomLevel) {
        this.setValue(this._dojoZoomLevel);
      }
    }

    /**
     * dojoの読み込みが完了したときのイベント
     *
     * @param {Object} event イベントオブジェクト
     * @param {Object} viewer dojoのviewerインスタンス
     */

  }, {
    key: '_onDojoImageLoadComplete',
    value: function _onDojoImageLoadComplete(event, viewer) {
      if (!this.isSliderReady) {
        this.isSliderReady = true;

        if (viewer && viewer._image && typeof viewer._image.width !== 'undefined') {
          var width = viewer._image.width;
          var height = viewer._image.height;
          if (!__WEBPACK_IMPORTED_MODULE_2__util__["e" /* isZoomableImage */](width, height)) {
            // 読み込んだ画像が正方形じゃない場合、ズームが正しく動かない可能性あり
            //console.warn('Zoom slider may not work properly because the image is not a square.');
          }
        }
      }
    }
  }]);

  return ZoomSlider;
}(__WEBPACK_IMPORTED_MODULE_0__base_slider__["a" /* BaseSlider */]);

/***/ })
/******/ ]);