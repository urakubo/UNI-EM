import {extendDojo} from './dojo-extension';
import {DojoGUI} from './dojo-gui';

(function() {
  if (window.DojoGUI) {
    return;
  }

  extendDojo();
  window.DojoGUI = new DojoGUI();
})();
