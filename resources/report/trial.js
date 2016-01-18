(function () {
    'use strict';

    var DATA = window.ANIM_DATA,
        paused = true,
        frameIndex = 0,
        animation_interval;

    function getLocator(name) {
        return $('#' + name);
    }

    function setLocatorValues(name, values) {
        var loc = getLocator(name);
        loc.attr({
            cx: DATA.scale * (values.x + DATA.offset[0]),
            cy: DATA.scale * (values.y + DATA.offset[1])
        });

        if (!loc.hasClass(values.annotation)) {
            loc.removeClass('FIXED MOVING');
            loc.addClass(values.annotation);
        }
    }

    function toDisplayNumber(value, unc) {
        return (0.01*Math.round(100.0*value)).toFixed(2) +
            ' &#177; ' +
            (0.01*Math.round(100.0*unc)).toFixed(2);
    }

    function updateStatusDisplay() {
        var frame = DATA.frames[frameIndex];

        DATA.markerIds.forEach(function (key, index) {
            var data = frame.positions[index],
                box = $('.status-box .entry.' + key);

            function formatForDisplay(value, unc) {
                return paused ? toDisplayNumber(value, unc) : '--';
            }

            box.find('.position.x').html(formatForDisplay(data.x, data.xunc));
            box.find('.position.y').html(formatForDisplay(data.y, data.yunc));
            box.find('.mode').html(paused ? data.annotation : '--');
        });
    }

    function onEnterFrame() {
        var i,
            keys = DATA.markerIds,
            frame = DATA.frames[frameIndex],
            progressBar = $('.progress-bar'),
            progress = 100.0*frameIndex/(DATA.time.count - 1),
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

        if (paused) { return; }

        frameIndex++;
        if (frameIndex >= DATA.time.count) { frameIndex = 0; }
    }

    function onPlaybackControl(role) {
        var frameAdjust = 0;

        switch (role) {
            case 'toggle-play':
                paused = !paused;
                $('.play-icon').toggle(paused);
                $('.pause-icon').toggle(!paused);
                window.clearInterval(animation_interval);
                updateStatusDisplay();
                if (!paused) {
                    animation_interval = window.setInterval(onEnterFrame, 100);
                }
                return;

            case 'jump-back':
                frameAdjust = -Math.floor(0.1*DATA.time.count);
                break;

            case 'jump-forward':
                frameAdjust = Math.floor(0.1*DATA.time.count);
                break;

            case 'frame-back':
                frameAdjust = -Math.max(1, Math.floor(0.01*DATA.time.count));
                break;

            case 'frame-forward':
                frameAdjust = Math.max(1, Math.floor(0.01*DATA.time.count));
                break;

            default:
                console.log('Unrecognized button role:', role);
                return;
        }

        frameIndex = Math.max(0, Math.min(
            DATA.time.count - 1,
            frameIndex + frameAdjust));

        updateStatusDisplay();
        if (paused) { onEnterFrame(); }
    }

    function populateCycleDisplay() {
        Object.keys(DATA.cycles).forEach(function (key) {
            var box = $('.cycles.' + key);
            DATA.cycles[key].forEach(function (cycle) {
                var e = $('<div class="cycle-box"></div>'),
                    width = 100.0*cycle.steps/DATA.time.count;
                e.css({width:width + '%'});

                if (cycle.key === 'MOVING') {
                    e.addClass(cycle.key);
                } else {
                    e.addClass(key + '_color');
                }

                e.appendTo(box);
            });
        });
    }

    function createPlots() {
        var element, elements = [];

        function makeScatterData(x, y, yUnc) {
            return [{
                x: x,
                y: y,
                error_y: { type: 'data', array: yUnc, visible: true },
                type: 'scatter'
              }
            ];
        }

        function makeLayout(title, xLabel, yLabel) {
            return {
              title: title,
              xaxis: {
                title: xLabel,
                titlefont: {
                  family: 'Courier New, monospace',
                  size: 18,
                  color: '#7f7f7f'
                }
              },
              yaxis: {
                title: yLabel,
                titlefont: {
                  family: 'Courier New, monospace',
                  size: 18,
                  color: '#7f7f7f'
                }
              }
            };
        }

        // GAL Plot
        element = document.getElementById('gal-plot');
        elements.push(element);
        Plotly.newPlot(
            element,
            makeScatterData(
                DATA.time.progress,
                DATA.gals.values,
                DATA.gals.uncertainties),
            makeLayout(
                'Calculated Glenoacetabular Lengths',
                'Progress (%)',
                'Length (m)'
            )
        );

        // Left Extension Plot
        element = document.getElementById('left-extension-plot');
        elements.push(element);
        Plotly.newPlot(
            element,
            makeScatterData(
                DATA.time.progress,
                DATA.extensions.left.values,
                DATA.extensions.left.uncertainties),
            makeLayout(
                'Left Pes-Manus Extension Distances',
                'Progress (%)',
                'Distance (m)'
            )
        );

        // Right Extension Plot
        element = document.getElementById('right-extension-plot');
        elements.push(element);
        Plotly.newPlot(
            element,
            makeScatterData(
                DATA.time.progress,
                DATA.extensions.right.values,
                DATA.extensions.right.uncertainties),
            makeLayout(
                'Right Pes-Manus Extension Distances',
                'Progress (%)',
                'Distance (m)'
            )
        );

        // Back Extension Plot
        element = document.getElementById('back-extension-plot');
        elements.push(element);
        Plotly.newPlot(
            element,
            makeScatterData(
                DATA.time.progress,
                DATA.extensions.back.values,
                DATA.extensions.back.uncertainties),
            makeLayout(
                'Pes-Pes Extension Distances',
                'Progress (%)',
                'Distance (m)'
            )
        );

        // Front Extension Plot
        element = document.getElementById('front-extension-plot');
        elements.push(element);
        Plotly.newPlot(
            element,
            makeScatterData(
                DATA.time.progress,
                DATA.extensions.front.values,
                DATA.extensions.front.uncertainties),
            makeLayout(
                'Manus-Manus Extension Distances',
                'Progress (%)',
                'Distance (m)'
            )
        );

        window.onresize = function() {
            elements.forEach(function(e) {
                Plotly.Plots.resize(e);
            });
        };
    }

    function initialize_results_display() {
        var box = $('.settings-box');

        function setValue(id, result) {
            box.find('.' + id).html(result);
        }

        setValue('gal-value', DATA.gals.result);
        setValue('left-extension-value', DATA.extensions.left.result);
        setValue('right-extension-value', DATA.extensions.right.result);
        setValue('front-extension-value', DATA.extensions.front.result);
        setValue('back-extension-value', DATA.extensions.back.result);
    }

    $(function () {
        var controlBar = $('.playback-controls');

        initialize_results_display();
        createPlots();

        controlBar.find('.control').click(function (event) {
            onPlaybackControl($(event.currentTarget).attr('data-role'));
        });
        controlBar.find('.play-icon').hide();

        populateCycleDisplay();
        onPlaybackControl('toggle-play');
    });

}());
