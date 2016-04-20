(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    exports.LIMB_COLORS = {
        left_pes: 'DodgerBlue',
        right_pes: 'DarkOrange',
        left_manus: 'DarkOliveGreen',
        right_manus: 'DarkOrchid'
    };

    function drawMidline() {
        var lineMaker = d3.svg.line()
            .x(function (frame) {
                return exports.DATA.scale * frame.midpoint.x[2];
            })
            .y(function (frame) {
                return -exports.DATA.scale * frame.midpoint.y[2];
            })
            .interpolate('linear');

        d3.select($('.svg-box svg')[0])
            .append('path')
            .attr('d', lineMaker(exports.DATA.frames))
            .style('stroke', 'rgba(0, 0, 0, 0.1)')
            .style('stroke-dasharray', '2,2')
            .style('stroke-width', '2')
            .style('fill', 'transparent');
    }
    exports.drawMidline = drawMidline;

    function initialize_animation() {
        var root = d3.select($('.svg-box svg')[0]);

        root.append('line')
            .attr('id', 'left_pes_coupling')
            .style('stroke', 'rgba(0, 0, 0, 0.1)')
            .style('stroke-width', '2');

        root.append('line')
            .attr('id', 'right_pes_coupling')
            .style('stroke', 'rgba(0, 0, 0, 0.1)')
            .style('stroke-width', '2');

        root.append('line')
            .attr('id', 'left_manus_coupling')
            .style('stroke', 'rgba(0, 0, 0, 0.1)')
            .style('stroke-width', '2');

        root.append('line')
            .attr('id', 'right_manus_coupling')
            .style('stroke', 'rgba(0, 0, 0, 0.1)')
            .style('stroke-width', '2');

        root.append('line')
            .attr('id', 'coupling_length')
            .style('stroke', 'rgba(0, 0, 0, 0.1)')
            .style('stroke-width', '2');

        root.append('circle')
            .attr('id', 'rear_coupler')
            .attr('r', 4)
            .style('fill', 'rgb(100, 100, 100)');

        root.append('circle')
            .attr('id', 'forward_coupler')
            .attr('r', 4)
            .style('fill', 'rgb(100, 100, 100)');

        root.append('circle')
            .attr('id', 'left_pes_pin')
            .attr("r", 4)
            .style("fill", exports.LIMB_COLORS.left_pes);

        root.append('circle')
            .attr('id', 'right_pes_pin')
            .attr("r", 4)
            .style("fill", exports.LIMB_COLORS.right_pes);

        root.append('circle')
            .attr('id', 'left_manus_pin')
            .attr("r", 4)
            .style("fill", exports.LIMB_COLORS.left_manus);

        root.append('circle')
            .attr('id', 'right_manus_pin')
            .attr("r", 4)
            .style("fill", exports.LIMB_COLORS.right_manus);

        root.append('circle')
            .attr('id', 'right_manus_pin')
            .attr("r", 4)
            .style("fill", exports.LIMB_COLORS.right_manus);
    }
    exports.initialize_animation = initialize_animation;

    function getLocator(name) {
        return $('#' + name);
    }

    function setLocatorValues(name, values) {
        var loc = getLocator(name);
        var pin = getLocator(name + '_pin');
        var css = exports.ANNOTATIONS[values.f];

        loc.attr({
            cx: exports.DATA.scale * values.x[2],
            cy: -exports.DATA.scale * values.y[2]
        });

        pin.attr({
            cx: exports.DATA.scale * values.x[2],
            cy: -exports.DATA.scale * values.y[2]
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

        d3.select(getLocator('left_pes_coupling')[0])
            .attr('x1', exports.DATA.scale * frame.positions[0].x[2])
            .attr('y1', -exports.DATA.scale * frame.positions[0].y[2])
            .attr('x2', exports.DATA.scale * frame.rear_coupler.x[2])
            .attr('y2', -exports.DATA.scale * frame.rear_coupler.y[2]);

        d3.select(getLocator('right_pes_coupling')[0])
            .attr('x1', exports.DATA.scale * frame.positions[1].x[2])
            .attr('y1', -exports.DATA.scale * frame.positions[1].y[2])
            .attr('x2', exports.DATA.scale * frame.rear_coupler.x[2])
            .attr('y2', -exports.DATA.scale * frame.rear_coupler.y[2]);

        d3.select(getLocator('left_manus_coupling')[0])
            .attr('x1', exports.DATA.scale * frame.positions[2].x[2])
            .attr('y1', -exports.DATA.scale * frame.positions[2].y[2])
            .attr('x2', exports.DATA.scale * frame.forward_coupler.x[2])
            .attr('y2', -exports.DATA.scale * frame.forward_coupler.y[2]);

        d3.select(getLocator('right_manus_coupling')[0])
            .attr('x1', exports.DATA.scale * frame.positions[3].x[2])
            .attr('y1', -exports.DATA.scale * frame.positions[3].y[2])
            .attr('x2', exports.DATA.scale * frame.forward_coupler.x[2])
            .attr('y2', -exports.DATA.scale * frame.forward_coupler.y[2]);

        d3.select(getLocator('coupling_length')[0])
            .attr('x1', exports.DATA.scale * frame.rear_coupler.x[2])
            .attr('y1', -exports.DATA.scale * frame.rear_coupler.y[2])
            .attr('x2', exports.DATA.scale * frame.forward_coupler.x[2])
            .attr('y2', -exports.DATA.scale * frame.forward_coupler.y[2]);

        d3.select(getLocator('rear_coupler')[0])
            .attr('cx', exports.DATA.scale * frame.rear_coupler.x[2])
            .attr('cy', -exports.DATA.scale * frame.rear_coupler.y[2]);

        d3.select(getLocator('forward_coupler')[0])
            .attr('cx', exports.DATA.scale * frame.forward_coupler.x[2])
            .attr('cy', -exports.DATA.scale * frame.forward_coupler.y[2]);

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
