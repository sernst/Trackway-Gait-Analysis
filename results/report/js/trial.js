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
     * @param lower
     * @returns {*|string|XML|void}
     */
    function capitalize(lower) {
        return (lower ? this.toLowerCase() : this)
            .replace(/(?:^|\s)\S/g, function(a) {
                return a.toUpperCase();
            });
    }
    exports.capitalize = capitalize;

    /**
     *
     * @param value
     * @param unc
     * @returns {string}
     */
    function toDisplayNumber(value, unc) {
        return (0.01*Math.round(100.0*value)).toFixed(2) +
            ' &#177; ' +
            (0.01*Math.round(100.0*unc)).toFixed(2);
    }

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
                    toDisplayNumber(value, unc) :
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

    /**
     *
     */
    function initializeResultsDisplay() {
        var box = $('#lengthResults');

        function setValue(label, entry) {
            var e = $('<div></div>');
            $('<span></span>')
                .addClass('label')
                .html(label + ': ')
                .appendTo(e);

            $('<span></span>')
                .addClass('value')
                .html(entry.result)
                .appendTo(e);

            $('<span></span>')
                .addClass('deviation-value')
                .addClass(entry.deviation_max <= 2.0 ? 'low' : 'high')
                .html(entry.deviation_max + '&sigma;')
                .appendTo(e);

            box.append(e);
        }

        setValue('Coupling Distance', exports.DATA.gals);
        setValue('LP-LM Separation', exports.DATA.separations.left);
        setValue('RP-RM Separation', exports.DATA.separations.right);
        setValue('LP-RP Separation', exports.DATA.separations.back);
        setValue('LM-RM Separation', exports.DATA.separations.front);
        setValue('LP Extension', exports.DATA.extensions.left_pes);
        setValue('RP Extension', exports.DATA.extensions.right_pes);
        setValue('LM Extension', exports.DATA.extensions.left_manus);
        setValue('RM Extension', exports.DATA.extensions.right_manus);
    }
    exports.initializeResultsDisplay = initializeResultsDisplay;

}());
