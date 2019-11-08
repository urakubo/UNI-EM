/**
 * sliderの基底クラス
 */
export class BaseSlider {

  get template() {
    return _.template(`<input type="text">`);
  }

  constructor() {
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

  initSlider() {
    if (this.initialized) {
      return;
    }
    this.initialized = true;

    this.el = $(this.template());
    this.wrapperEl.append(this.el);

    const sliderOptions = Object.assign({}, {
      min: this.sliderMin,
      max: this.sliderMax,
      step: this.sliderStep,
      value: this.sliderValue,
      formatter: (...args) => this.sliderFormatter(...args)
    }, this.sliderOptions || {});

    this.el.bootstrapSlider(sliderOptions).on('change', (...args) => {
      this.onSliderChange(...args);
    });
  }

  sliderFormatter(value) {
    return `${value}/${this.sliderMax}`;
  }

  onSliderChange(event) {
  }

  getValue() {
    return this.el.bootstrapSlider('getValue');
  }

  setValue(value) {
    return this.el.bootstrapSlider('setValue', value);
  }
}
