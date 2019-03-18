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
export const DOJO_CANVAS_BUFFER_WIDTH = 512;

// canvasの高さ
export const DOJO_CANVAS_BUFFER_HEIGHT = 512;


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
export const SLICE_SLIDER_MIN_VALUE = 1;

// sliceスライダーを動かすといくつ動くか
export const SLICE_SLIDER_STEP = 1;

// sliceスライダーの初期値
export const SLICE_SLIDER_DEFAULT_VALUE = 1;

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
export const OPACITY_SLIDER_MIN_VALUE = 0;

// opacityスライダーの最大値
export const OPACITY_SLIDER_MAX_VALUE = 255;

// opacityスライダーを動かすといくつ動くか
export const OPACITY_SLIDER_STEP = 20;

// opacityスライダーの初期値
export const OPACITY_SLIDER_DEFAULT_VALUE = 100;

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
export const ZOOM_SLIDER_MIN_VALUE = 1;

// zoomスライダーの最大値
// 本来camera.jsのfuture_zoom_levelを使うが、バグがあるため
// 初期状態から何回ズームできるかを単純に数えた数
export const ZOOM_SLIDER_MAX_VALUE = 13;

// zoomスライダーを動かすといくつ動くか
export const ZOOM_SLIDER_STEP = 1;

// zoomスライダーの初期値
export const ZOOM_SLIDER_DEFAULT_VALUE = 2;
