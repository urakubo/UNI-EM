// 汎用ユーティリティなど

import * as config from './config';

/**
 * keydownイベントを発火する
 *
 * @param  {number} keyCode 発火するキーコード
 */
export function triggerKeydown(keyCode) {
  const event = $.Event('keydown');
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
export function addAfter(target, name, after) {
  const original = target[name];
  target[name] = function() {
    const result = original.apply(this, arguments);
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
export function getWindowCenterPos() {
  const x = Math.floor($(window).width() / 2);
  const y = Math.floor($(window).height() / 2);

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
export function getCameraCenterPos() {
  const centerX = DOJO.viewer._width / 2;
  const centerY = DOJO.viewer._height / 2;

  const canvasLeft = centerX - config.DOJO_CANVAS_BUFFER_WIDTH / 2;
  const canvasRight = canvasLeft + config.DOJO_CANVAS_BUFFER_WIDTH;
  const canvasTop = centerY - config.DOJO_CANVAS_BUFFER_HEIGHT / 2;
  const canvasBottom = canvasTop + config.DOJO_CANVAS_BUFFER_HEIGHT;

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
export function isOverImage(x, y) {
  const u_v = DOJO.viewer.xy2uv(x, y);
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
export function isZoomableImage(canvasImageWidth, canvasImageHeight) {
  const half = canvasImageHeight / 2;
  return canvasImageWidth - half > 0;
}

