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

    /**
     *
     */
    function add_svg_tooltips() {
        var div = window.d3.select("body")
            .append("div")
            .attr("class", "track-pos-tooltip")
            .style("opacity", 0);

        $('.svg-box .track-pos')
            .on("mouseover", function (event) {

                var w = $(window).width();
                var horizontal = event.pageX;
                var on_left = (w - horizontal) >= 250;
                if (!on_left) {
                    horizontal = w - horizontal;
                }

                var e = $(event.currentTarget);

                div.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                div.html(e.attr('data-name') + "<br/>" + e.attr('data-uid'))
                    .style('left', null)
                    .style('right', null)
                    .style(on_left ? "left" : "right", (horizontal) + "px")
                    .style('width', '250px')
                    .style("top", (event.pageY - 28) + "px")
                    .style('background-color', e.attr('data-color'));
            })
            .on("mouseout", function () {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
    }
    exports.add_svg_tooltips = add_svg_tooltips;

}());
