import * as util from './util';

// GUI化するために必要なdojoの機能拡張

let extended = false;

export function extendDojo() {
  if (extended) {
    return;
  }
  extended = true;

  /**
   * Loading用拡張
   */

  // Loading開始/完了時にフック用イベントを追加する
  util.addAfter(J.viewer.prototype, 'loading', function() {
    const isReady = this._image_buffer_ready;
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
    slice_seek(n) {
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
      const oldZ = this._z;
      this._z = n - 1;

      this._loader.load_tiles(this._x, this._y, this._z, this._w, this._w, false);

      if (DOJO.threeD) {
        // 3D Viewerを表示してるときの赤い線を移動する
        let count = this._z - oldZ;
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
  util.addAfter(DOJO, 'update_slice_number', function(n) {
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
    set_opacity(n) {
      this._overlay_opacity = Math.min(255, Math.max(0, n));
      this.redraw();
    }
  });

  // opacityが変わった後にイベントを発行する
  util.addAfter(J.viewer.prototype, 'increase_opacity', function() {
    EventBus.dispatch('DOJO:opacityChange', null, this._overlay_opacity);
  });

  util.addAfter(J.viewer.prototype, 'decrease_opacity', function() {
    EventBus.dispatch('DOJO:opacityChange', null, this._overlay_opacity);
  });

  /**
   * Zoom用拡張
   */

   Object.assign(J.camera.prototype, {
    // J.camera.prototype.centerと同じ処理
    fix_center() {
      let diff = this._viewer._image.width - this._viewer._image.height / 2;
      if (diff > 0) {
        diff = 0;
      } else {
        // 1pxずらして中央位置の基点をずらし、ズームできるようにする
        diff--;
      }
      this._view[6] = this._viewer._width/2 - 512/2 - diff;
      this._view[7] = this._viewer._height/2 - 512/2;
    }
  });

  // zoom時にスライダーと動きを連動させるためにフック用イベントを追加する
  util.addAfter(J.camera.prototype, 'zoom', function(x, y, delta) {
    var u_v = this._viewer.xy2uv(x,y);
    // マウスカーソルがcanvas上じゃなかった場合は実際にズームされないのでスキップ
    if (u_v[0] == -1 || u_v[1] == -1) {
      return;
    }

    // zoomレベルの取得方法、違う可能性あり
    // this._view[4]で合ってるか?
    // 3回くらい拡大すると一旦future_zoom_levelがリセットされてしまうため値がおかしくなる
    // dojo側のバグ?
    const future_zoom_level = this._view[4];
    EventBus.dispatch('DOJO:zoomChange', null, x, y, delta, future_zoom_level);
  });


  /**
   * Marge, Split Modeに切り替わったとき、オフになったときにフック用イベントを追加する
   */
  util.addAfter(DOJO, 'reset_tools', function() {
    EventBus.dispatch('DOJO:resetTools', null);
  });

  util.addAfter(J.controller.prototype, 'merge', function(id) {
    EventBus.dispatch('DOJO:merge', null, id);
  });

  util.addAfter(J.controller.prototype, 'start_split', function(id, x, y) {
    EventBus.dispatch('DOJO:startSplit', null, id, x, y);
  });


  /**
   * その他の拡張
   */

  // 読み込み時/読み込み完了にフック用イベントを追加する
  util.addAfter(J.viewer.prototype, 'loading', function(value) {
    if (this._image_buffer_ready) {
      EventBus.dispatch('DOJO:imageLoadComplete', null, this);
    } else {
      EventBus.dispatch('DOJO:imageLoadStart', null, this);
    }
  });
}
