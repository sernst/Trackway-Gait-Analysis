(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;


    function onPlaybackControl(role) {
        var frameAdjust = 0;

        switch (role) {
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

            case 'jump-back':
                frameAdjust = -Math.floor(0.1*exports.DATA.time.count);
                break;

            case 'jump-forward':
                frameAdjust = Math.floor(0.1*exports.DATA.time.count);
                break;

            case 'frame-back':
                frameAdjust = -Math.max(1, Math.floor(
                    0.01*exports.DATA.time.count));
                break;

            case 'frame-forward':
                frameAdjust = Math.max(1, Math.floor(
                    0.01*exports.DATA.time.count));
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
