import {BaseSlider} from './base-slider';
import * as config from './config';
import * as util from './util';

export class SliceSlider extends BaseSlider {
  constructor() {
    super();

    this._targetSliceNumber = null;
    this._isSeeking = false;
    this._seekQueue = [];

    this.sliderMin = config.SLICE_SLIDER_MIN_VALUE;
    this.sliderStep = config.SLICE_SLIDER_STEP;
    this.sliderValue = config.SLICE_SLIDER_DEFAULT_VALUE;

    this.wrapperEl = $('.gui-slice-wrapper');
    this.sliderOptions = {};

    EventBus.addEventListener('DOJO:sliceNumberChange', (...args) => {
      this._onDojoSliceNumberChange(...args);
    });
    EventBus.addEventListener('DOJO:imageLoadComplete', (...args) => {
      this._onDojoImageLoadComplete(...args);
    });
  }

  sliderFormatter(value) {
    // DOJO.update_slice_numberに合わせて-1の値にする
    return `${value - 1}/${this.sliderMax - 1}`;
  }

  /**
   * スライダーをcameraと同じ位置に置く
   */
  setWrapperPositon() {
    const { left, bottom } = util.getCameraCenterPos();

    // 横位置をcameraと同じに揃える
    const wrapperLeft = left;
    // 縦位置をcameraのすぐ下に揃える
    const wrapperTop = bottom + 20;

    // スライダーを表示する
    this.wrapperEl.css({
      left: wrapperLeft,
      top: wrapperTop
    }).show();
  }

  isSlicing() {
    return this._targetSliceNumber != null;
  }

  sliceSeek(value) {
    return new Promise((resolve, reject) => {
      this._targetSliceNumber = value;
      DOJO.viewer._camera.slice_seek(value);

      // dojo本体のslice numberが更新されるまで待機する
      chillout.till(() => {
        if (!this.isSlicing()) {
          return false; // stop iteration
        }
      }).then(() => {
        resolve();
      });
    });
  }

  onSliderChange(event) {
    const { oldValue, newValue } = event.value;

    // スライス途中だったら無視する
    if (this.isSlicing()) {
      event.preventDefault();
      this.setValue(oldValue);
      return;
    }

    // 動かしてる途中だったら処理が重ならないようにする
    const seek = () => {
      this._isSeeking = true;
      this.sliceSeek(newValue).then(() => {
        if (this._seekQueue.length > 0) {
          // シークのつまみを早く動かした場合、つまみを動かした分すべて実行するとカクカクと重くなるので
          // 不要な処理を除外する。最後の動きだけがあれば十分と思われる
          // 2コマ以上あったら捨てていく
          while (this._seekQueue.length > 2) {
            this._seekQueue.shift();
          }

          const queue = this._seekQueue.shift();
          queue();
        }
        this._isSeeking = false;
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
  _onDojoSliceNumberChange(event, n, maxZTiles) {
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

    const value = this.getValue();
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
  _onDojoImageLoadComplete(event, viewer) {
    if (!this.isSliderReady) {
      // スライダーの最大値を読み込んだイメージから取得する
      this.sliderMax = DOJO.viewer._image.max_z_tiles;
      this.initSlider();
      this.setWrapperPositon();
      this.isSliderReady = true;
    }
  }
}
