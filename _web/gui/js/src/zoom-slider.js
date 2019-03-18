import {BaseSlider} from './base-slider';
import * as config from './config';
import * as util from './util';

export class ZoomSlider extends BaseSlider {
  constructor() {
    super();

    this._zoomBySlider = false;

    // dojoのzoomで設定されるべきfuture_zoom_levelの値にバグ?があるため
    // このクラス内でzoom回数をレベルとしてカウントする
    this._dojoZoomLevel = 1;

    this.sliderMin = config.ZOOM_SLIDER_MIN_VALUE;
    this.sliderMax = config.ZOOM_SLIDER_MAX_VALUE;
    this.sliderStep = config.ZOOM_SLIDER_STEP;
    this.sliderValue = config.ZOOM_SLIDER_DEFAULT_VALUE;

    this.wrapperEl = $('.gui-zoom-wrapper');
    this.sliderOptions = {
      precision: 1,
      tooltip: 'hide',
      tooltip_position: 'bottom'
    };
    this.initSlider();

    EventBus.addEventListener('DOJO:zoomChange', (...args) => {
      this._onDojoZoomChange(...args);
    });
    EventBus.addEventListener('DOJO:imageLoadComplete', (...args) => {
      this._onDojoImageLoadComplete(...args);
    });
  }

  sliderFormatter(value) {
    return '';
  }

  zoomIn() {
    this.setZoom(1);
  }

  zoomOut() {
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
  setZoom(delta) {
    const { x, y } = util.getWindowCenterPos();

    DOJO.viewer._camera._x = x;
    DOJO.viewer._camera._y = y;
    DOJO.viewer._camera._i_j = DOJO.viewer.xy2ij(x, y);
    DOJO.viewer._camera.zoom(x, y, delta);
  }

  onSliderChange(event) {
    const { oldValue, newValue } = event.value;

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
  fixCenterPos() {
    const { x, y } = util.getWindowCenterPos();

    if (!util.isOverImage(x, y)) {
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
  _onDojoZoomChange(event, x, y, delta, future_zoom_level) {
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

    const value = this.getValue();
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
  _onDojoImageLoadComplete(event, viewer) {
    if (!this.isSliderReady) {
      this.isSliderReady = true;

      if (viewer && viewer._image && typeof viewer._image.width !== 'undefined') {
        const width = viewer._image.width;
        const height = viewer._image.height;
        if (!util.isZoomableImage(width, height)) {
          // 読み込んだ画像が正方形じゃない場合、ズームが正しく動かない可能性あり
          //console.warn('Zoom slider may not work properly because the image is not a square.');
        }
      }
    }
  }
}
