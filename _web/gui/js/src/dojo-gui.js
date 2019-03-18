import {HeaderToolbar} from './header-toolbar';
import {SliceSlider} from './slice-slider';
import {OpacitySlider} from './opacity-slider';
import {ZoomSlider} from './zoom-slider';

export class DojoGUI {
  constructor() {
    this._elementsInitialized = false;
  }

  init() {
    EventBus.addEventListener('DOJO:loading', (...args) => this.onDojoLoading(...args));
    EventBus.addEventListener('DOJO:merge', (...args) => this.onDojoMerge(...args));
    EventBus.addEventListener('DOJO:startSplit', (...args) => this.onDojoStartSplit(...args));
    EventBus.addEventListener('DOJO:resetTools', (...args) => this.onDojoResetTools(...args));
  }

  onDojoLoading(event, isReady) {
    if (isReady && !this._elementsInitialized) {
      this._elementsInitialized = true;
      this.initElements();
    }
  }

  initElements() {
    this.headerToolbar = new HeaderToolbar();
    this.sliceSlider = new SliceSlider();
    this.opacitySlider = new OpacitySlider();
    this.zoomSlider = new ZoomSlider();
  }

  /**
   * camera用のスライダーを有効化
   */
  enableCameraSliders() {
    this.sliceSlider.el.bootstrapSlider('enable');
    this.zoomSlider.el.bootstrapSlider('enable');
  }

  /**
   * camera用のスライダーを無効化
   */
  disableCameraSliders() {
    this.sliceSlider.el.bootstrapSlider('disable');
    this.zoomSlider.el.bootstrapSlider('disable');
  }

  /**
   * Margeモードに切り替わった時のイベント
   *
   * @param  {Object} event イベントオブジェクト
   * @param  {number} id    merge時に渡されるパラメータ
   */
  onDojoMerge(event, id) {
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
  onDojoStartSplit(event, id, x, y) {
    this.disableCameraSliders();
  }

  /**
   * DOJO.reset_toolsが実行された時のイベント
   *
   * @param  {Object} event イベントオブジェクト
   */
  onDojoResetTools() {
    this.enableCameraSliders();
  }
}
