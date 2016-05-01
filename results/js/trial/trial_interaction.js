(function () {
  'use strict';

  var exports = window.SIM || {};
  window.SIM = exports;

  var _poppedOut = false;

  function popOutSvg() {
    var e = $('.svg-box');

    if (_poppedOut) {
      e.removeAttr('style');
      e.find('.svg-controls-box').hide();
      _poppedOut = false;
      return;
    }

    _poppedOut = true;
    e.css({
      position: 'fixed',
      top: '10px',
      left: '10px',
      width: '66%',
      'background-color': 'white',
      border: '1px solid rgba(0, 0, 0, 0.3)',
      'z-index': 9000
    });
    e.find('.svg-controls-box').show();
  }
  exports.popOutSvg = popOutSvg;

  function saveSvg() {
    var wasPaused = exports.animation.paused;
    var frame = exports.DATA.frames[exports.animation.frameIndex];

    exports.animation.paused = true;

    try {
      var isFileSaverSupported = !!new Blob();
    } catch (e) {
      alert("Save not supported on this browser");
    }

    var cycle = Math.floor(frame.time);
    var phase = Math.round(100.0 * (frame.time - cycle));

    var time = 'C' + cycle + 'p' + phase;
    var title = $('title').html().replace(/\s/g, '-') + '_' + time;

    var html = d3.select($('.svg-box svg')[0])
      .attr("title", title)
      .node().parentNode.innerHTML;

    var blob = new Blob([html], {type: "image/svg+xml"});
    window.saveAs(blob, title + ".svg");

    exports.animation.paused = wasPaused;
  }
  exports.saveSvg = saveSvg;

  /**
   * A callback executed by clicking on one of the playback control buttons
   * in the animation header section of the trial page. The action taken
   * during the callback depends on the specified role argument.
   *
   * @param role
   *  The specific role of the playback control that was clicked. Each role
   *  is handled differently
   */
  function onPlaybackControl(role) {
    var frameAdjust = 0;

    switch (role) {
      case 'pop-out':
        return exports.popOutSvg();

      case 'save-svg':
        return exports.saveSvg();

      case 'toggle-play':
        exports.animation.paused = !exports.animation.paused;
        $('.play-icon').toggle(exports.animation.paused);
        $('.pause-icon').toggle(!exports.animation.paused);
        window.clearInterval(exports.animation.interval);
        exports.updateStatusDisplay();

        if (!exports.animation.paused) {
          exports.animation.interval = window.setInterval(
            exports.onEnterFrame, 100);
        }
        return;

      case 'backward-10':
        frameAdjust = -Math.max(1, Math.floor(0.1 * exports.DATA.time.count));
        break;

      case 'forward-10':
        frameAdjust = Math.max(1, Math.floor(0.1 * exports.DATA.time.count));
        break;

      case 'jump-back':
        frameAdjust = -Math.max(
            1, Math.round(0.5 * exports.DATA.time.steps_per_cycle)
        );
        break;

      case 'jump-forward':
        frameAdjust = Math.max(
            1, Math.round(0.5 * exports.DATA.time.steps_per_cycle)
        );
        break;

      case 'frame-back':
        frameAdjust = -1;
        break;

      case 'frame-forward':
        frameAdjust = 1
        break;

      default:
        console.log('Unrecognized button role:', role);
        return;
    }

    exports.animation.frameIndex = Math.max(0, Math.min(
      exports.DATA.time.count - 1,
      exports.animation.frameIndex + frameAdjust));

    exports.updateStatusDisplay();
    if (exports.animation.paused) {
      exports.onEnterFrame();
    }
  }
  exports.onPlaybackControl = onPlaybackControl;

}());
