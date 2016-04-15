(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    function getLocator(name) {
        return $('#' + name);
    }

    function setLocatorValues(name, values) {
        var loc = getLocator(name);
        var css = exports.ANNOTATIONS[values.f];

        loc.attr({
            cx: exports.DATA.scale * values.x[0],
            cy: -exports.DATA.scale * values.y[0]
        });

        if (!loc.hasClass(css)) {
            loc.removeClass('FIXED MOVING');
            loc.addClass(css);
        }
    }

    function onEnterFrame() {
        var i,
            keys = exports.DATA.markerIds,
            frame = exports.DATA.frames[exports.animation.frameIndex],
            progressBar = $('.progress-bar'),
            progress = 100.0*exports.animation.frameIndex /
                (exports.DATA.time.count - 1),
            cycle = Math.floor(frame.time);

        progressBar.find('.inner').width(progress + '%');
        progressBar.find('.progress-value').html(Math.round(progress) + '%');
        progressBar.find('.cycle-value').html(cycle);
        progressBar.find('.phase-value').html(
            Math.round(100.0*(frame.time - cycle)) + '%&nbsp;'
        );

        for (i = 0; i < 4; i++) {
            setLocatorValues(keys[i], frame.positions[i]);
        }

        if (exports.animation.paused) {
            return;
        }

        exports.animation.frameIndex++;
        if (exports.animation.frameIndex >= exports.DATA.time.count) {
            exports.animation.frameIndex = 0;
        }
    }
    exports.onEnterFrame = onEnterFrame;

}());
