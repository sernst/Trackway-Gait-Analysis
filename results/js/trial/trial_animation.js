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


  /**
   *
   */
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
      .style('stroke-dasharray', '4,3')
      .style('stroke-width', '2')
      .style('fill', 'transparent')
      .style('pointer-events', 'none');
  }
  exports.drawMidline = drawMidline;


  /**
   *
   * @returns {*}
   */
  function boxPathDrawer() {
    return d3.svg.line()
        .x(function (point) {
          return exports.DATA.scale * point.x;
        })
        .y(function (point) {
          return -exports.DATA.scale * point.y;
        })
        .interpolate('linear');
  }


  /**
   *
   */
  function initialize_animation() {
    var root = d3.select($('.svg-box svg')[0]);

    root.append('line')
      .attr('id', 'left_pes_coupling')
      .classed('pes-coupling-assembly', true)
      .style('stroke', 'rgba(0, 0, 0, 0.1)')
      .style('stroke-width', '2')
      .style('pointer-events', 'none');

    root.append('line')
      .attr('id', 'right_pes_coupling')
      .classed('pes-coupling-assembly', true)
      .style('stroke', 'rgba(0, 0, 0, 0.1)')
      .style('stroke-width', '2')
      .style('pointer-events', 'none');

    root.append('line')
      .attr('id', 'left_manus_coupling')
      .classed('manus-coupling-assembly', true)
      .style('stroke', 'rgba(0, 0, 0, 0.1)')
      .style('stroke-width', '2')
      .style('pointer-events', 'none');

    root.append('line')
      .attr('id', 'right_manus_coupling')
      .classed('manus-coupling-assembly', true)
      .style('stroke', 'rgba(0, 0, 0, 0.1)')
      .style('stroke-width', '2')
      .style('pointer-events', 'none');

    root.append('line')
      .attr('id', 'coupling_length_pes')
      .classed('pes-coupling-assembly', true)
      .style('stroke', 'rgba(0, 0, 0, 0.1)')
      .style('stroke-width', '2')
      .style('pointer-events', 'none');

    root.append('line')
      .attr('id', 'coupling_length_manus')
      .classed('manus-coupling-assembly', true)
      .style('stroke', 'rgba(0, 0, 0, 0.1)')
      .style('stroke-width', '2')
      .style('pointer-events', 'none');

    root.append('path')
        .attr('id', 'rear_support_box')
        .style('fill', 'rgba(0, 0, 0, 0.25)')
        .style('pointer-events', 'none');

    root.append('path')
        .attr('id', 'forward_support_box')
        .style('fill', 'rgba(0, 0, 0, 0.25)')
        .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'rear_coupler')
      .classed('pes-coupling-assembly', true)
      .attr('r', 4)
      .style('fill', 'rgb(100, 100, 100)')
      .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'forward_coupler')
      .classed('manus-coupling-assembly', true)
      .attr('r', 4)
      .style('fill', 'rgb(100, 100, 100)')
      .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'geometric_center')
      .attr('r', 4)
      .style('fill', 'rgb(100, 100, 100)')
      .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'left_pes_pin')
      .attr("r", 4)
      .style("fill", exports.LIMB_COLORS.left_pes)
      .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'right_pes_pin')
      .attr("r", 4)
      .style("fill", exports.LIMB_COLORS.right_pes)
      .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'left_manus_pin')
      .attr("r", 4)
      .style("fill", exports.LIMB_COLORS.left_manus)
      .style('pointer-events', 'none');

    root.append('circle')
      .attr('id', 'right_manus_pin')
      .attr("r", 4)
      .style("fill", exports.LIMB_COLORS.right_manus)
      .style('pointer-events', 'none');
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


  /**
   *
   * @param type
   * @param time
   */
  function updateDisplayTime(type, time) {
    var cycle = Math.floor(time);
    var phase = '' + Math.round(100.0 * (time - cycle));

    while (phase.length < 2) {
      phase = '0' + phase;
    }
    phase += '%&nbsp;';

    var box = $('.' + type + '-time-box');
    box.find('.cycle-value').html(cycle);
    box.find('.phase-value').html(phase);

    $('.svg-box .' + type + '-status').html(cycle + ' : ' + phase);
  }


  /**
   *
   */
  function onEnterFrame() {
    var i, interpValue;
    var keys = exports.DATA.markerIds;
    var frame = exports.DATA.frames[exports.animation.frameIndex];
    var progressBar = $('.progress-bar');

    var progress = 100.0 * exports.animation.frameIndex / (
      exports.DATA.time.count - 1
    );

    var interpolator = d3.interpolateRgb(
      d3.rgb(40, 40, 40),
      d3.rgb(255, 60, 60)
    );

    progressBar.find('.inner').width(progress + '%');
    progressBar.find('.progress-value').html(Math.round(progress) + '%');

    updateDisplayTime('activity', frame.time);
    updateDisplayTime('support', frame.support_time);

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

    d3.select(getLocator('coupling_length_pes')[0])
      .attr('x1', exports.DATA.scale * frame.rear_coupler.x[2])
      .attr('y1', -exports.DATA.scale * frame.rear_coupler.y[2])
      .attr('x2', exports.DATA.scale * frame.midpoint.x[2])
      .attr('y2', -exports.DATA.scale * frame.midpoint.y[2]);

    d3.select(getLocator('coupling_length_manus')[0])
      .attr('x1', exports.DATA.scale * frame.midpoint.x[2])
      .attr('y1', -exports.DATA.scale * frame.midpoint.y[2])
      .attr('x2', exports.DATA.scale * frame.forward_coupler.x[2])
      .attr('y2', -exports.DATA.scale * frame.forward_coupler.y[2]);

    d3.select(getLocator('rear_support_box')[0])
      .attr('d', boxPathDrawer()(frame.rear_support_box));

    d3.select(getLocator('forward_support_box')[0])
      .attr('d', boxPathDrawer()(frame.forward_support_box));

    interpValue = Math.max(0, Math.min(1.0, 5 * Math.max(
       frame.rear_coupler.x[1],
       frame.rear_coupler.y[1]
    )));
    d3.select(getLocator('rear_coupler')[0])
      .attr('cx', exports.DATA.scale * frame.rear_coupler.x[2])
      .attr('cy', -exports.DATA.scale * frame.rear_coupler.y[2])
      .style('fill', interpolator(interpValue));

    interpValue = Math.max(0, Math.min(1.0, 5 * Math.max(
      frame.forward_coupler.x[1],
      frame.forward_coupler.y[1]
    )));
    d3.select(getLocator('forward_coupler')[0])
      .attr('cx', exports.DATA.scale * frame.forward_coupler.x[2])
      .attr('cy', -exports.DATA.scale * frame.forward_coupler.y[2])
      .style('fill', interpolator(interpValue));

    interpValue = Math.max(0, Math.min(1.0, 5 * Math.max(
       frame.midpoint.x[1],
       frame.midpoint.y[1]
    )));
    d3.select(getLocator('geometric_center')[0])
      .attr('cx', exports.DATA.scale * frame.midpoint.x[2])
      .attr('cy', -exports.DATA.scale * frame.midpoint.y[2])
      .style('fill', interpolator(interpValue));

    if (exports.animation.paused) {
      return;
    }

    exports.animation.frameIndex += 1;
    if (exports.animation.frameIndex >= exports.DATA.time.count) {
      exports.animation.frameIndex = 0;
    }
  }
  exports.onEnterFrame = onEnterFrame;

}());
