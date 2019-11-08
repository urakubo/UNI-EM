import {BaseSlider} from './base-slider';
import * as config from './config';

export class OpacitySlider extends BaseSlider {
  constructor() {
    super();

    this.sliderMin = config.OPACITY_SLIDER_MIN_VALUE;
    this.sliderMax = config.OPACITY_SLIDER_MAX_VALUE;
    this.sliderStep = config.OPACITY_SLIDER_STEP;
    this.sliderValue = config.OPACITY_SLIDER_DEFAULT_VALUE;

    this.wrapperEl = $('.gui-opacity-wrapper');
    this.sliderOptions = {
      tooltip_position: 'bottom'
    };
    this.initSlider();

    EventBus.addEventListener('DOJO:opacityChange', (...args) => {
      this._onDojoOpacityChange(...args);
    });
    this.isSliderReady = true;
  }

  setOpacity(opacity) {
    DOJO.viewer.set_opacity(opacity);
  }

  onSliderChange(event) {
    const { oldValue, newValue } = event.value;
    this.setOpacity(newValue);
  }

  /**
   * dojoのopacityが変わったときのイベント
   *
   * @param {Object} event イベントオブジェクト
   * @param {number} opacity 不透明度
   */
  _onDojoOpacityChange(event, opacity) {
    if (!this.isSliderReady) {
      return;
    }

    const value = this.getValue();
    if (value !== opacity) {
      this.setValue(opacity);
    }
  }
}
