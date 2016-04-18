(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    exports.ANNOTATIONS = {
        M: 'MOVING',
        F: 'FIXED'
    };

    exports.animation = {
        paused: true,
        frameIndex: 0,
        interval: null
    };

    /**
     *
     */
    function updateStatusDisplay() {
        var frame = exports.DATA.frames[exports.animation.frameIndex];

        exports.DATA.markerIds.forEach(function (key, index) {
            var data = frame.positions[index],
                box = $('.status-box .entry.' + key);

            function formatter(value, unc) {
                return exports.animation.paused ?
                    exports.toDisplayNumber(value, unc) :
                    '--';
            }

            box.find('.position.x').html(formatter(data.x[0], data.x[1]));
            box.find('.position.y').html(formatter(data.y[0], data.y[1]));
            box.find('.mode').html(
                exports.animation.paused ? exports.ANNOTATIONS[data.f] : '--');
        });
    }
    exports.updateStatusDisplay = updateStatusDisplay;

    /**
     *
     */
    function populateCycleDisplay() {
        Object.keys(exports.DATA.cycles).forEach(function (key) {

            var box = $('.cycles.' + key);

            exports.DATA.cycles[key].forEach(function (cycle) {
                var e = $('<div class="cycle-box"></div>');
                var width = 100.0*cycle[0]/exports.DATA.time.count;
                var css = exports.ANNOTATIONS[cycle[1]];
                e.css({width:width + '%'});

                if (css === 'MOVING') {
                    e.addClass(css);
                } else {
                    e.addClass(css + '_color');
                }

                e.appendTo(box);
            });
        });
    }
    exports.populateCycleDisplay = populateCycleDisplay;

}());
