import * as config from './config';

export class HeaderToolbar {

  constructor() {
    this.el = $('.gui-header-toolbar');
    this.infopanel = $('.infopanel');

    this.menu = this.el.find('.gui-menu');
    this.menu.on('click', (...args) => this.onMenuClick(...args));

    this.menuLabel = this.menu.find('.gui-menu-label');
  }

  onMenuClick(event) {
    return new Promise((resolve, reject) => {
      this.infopanel.slideToggle('fast').promise().done(() => {
        if (this.infopanel.is(':visible')) {
          this.menuLabel.text('Close Menu');
        } else {
          this.menuLabel.text('Open Menu');
        }
      });
    });
  }
}
