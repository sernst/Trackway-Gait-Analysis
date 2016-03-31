(function () {
    'use strict';

    var SIM = window.SIM || {};
    var exports = SIM.plot || {};
    SIM.plot = exports;
    window.SIM = SIM;

    var _elements = [];


    function refresh() {
        _elements.forEach(function(e) {
            Plotly.Plots.resize(e);
        });
    }
    exports.refresh = refresh;
    SIM.resizeCallbacks.push(exports.refresh);

    exports.colors = [
        [31, 119, 180],
        [255, 127, 14],
        [44, 160, 44],
        [214, 39, 40],
        [148, 103, 189],
        [140, 86, 75],
        [227, 119, 194],
        [127, 127, 127],
        [188, 189, 34],
        [23, 190, 207]
    ];

    /**
     *
     * @param index
     * @param opacity
     * @returns {string}
     */
    function getColor(index, opacity) {
        var c = exports.colors[index % exports.colors.length];
        if (!opacity) {
            return 'rgb(' + c.join(', ') + ')';
        }

        return 'rgba(' + c.join(', ') + ', ' + opacity + ')';
    }
    exports.getColor = getColor;

    /**
     *
     * @returns {Element}
     */
    function createElement(parent) {
        if (typeof parent === 'string' || parent instanceof String) {
            parent = $(parent);
        }

        var plotElement = $('<div></div>');

        plotElement.addClass('plot');
        if (parent) {
            plotElement.appendTo(parent);
        }
        _elements.push(plotElement[0]);

        return plotElement[0];
    }
    exports.createElement = createElement;

    /**
     *
     * @param dataSeries
     * @returns {{data: *, layout: {}}}
     */
    function makeLines(dataSeries) {
        var data = dataSeries.map(function (series) {
            return exports.makeLine(series.x, series.y, series.yUnc, {
                name: series.name
            }).data[0];
        });

        return {
            data: data,
            layout: {}
        };
    }
    exports.makeLines = makeLines;

    /**
     *
     * @param x
     * @param y
     * @param yUnc
     * @param args
     * @returns {{data: *[], layout: {}}}
     */
    function makeLine(x, y, yUnc, args) {
        var trace = args || {};
        trace.x = x;
        trace.y = y;
        trace.type = 'scatter';
        trace.mode = 'lines';

        if (yUnc) {
            trace.error_y = {type: 'data', array: yUnc, visible: true};
        }

        return {
            data:[trace],
            layout:{}
        };
    }
    exports.makeLine = makeLine;

    /**
     *
     * @param x
     * @param y
     * @param yUnc
     * @param mode
     * @returns {*[]}
     */
    function makeScatterData(x, y, yUnc, mode) {
        mode = mode || 'markers';
        var data = [{
            x: x,
            y: y,
            error_y: { type: 'data', array: yUnc, visible: true },
            type: 'scatter',
            mode: mode
          }
        ];

        return {
            data: data,
            layout: {}
        };
    }
    exports.makeScatterData = makeScatterData;

    /**
     *
     * @param x
     * @param y
     * @param yUnc
     * @returns {{data: *[], layout: {showlegend: boolean}}}
     */
    function makeContinuousLineData(x, y, yUnc) {
        var lower = [];
        var upper = [];
        y.forEach(function (yVal, index) {
            lower.push(yVal - yUnc[index]);
            upper.push(yVal + yUnc[index]);
        });

        var lowerTrace = {
            x: x,
            y: lower,
            line: {width: 0},
            marker: {color: "444"},
            mode: "lines",
            name: "Lower Bound",
            type: "scatter"
        };

        var middleTrace = {
            x: x,
            y: y,
            fill: "tonexty",
            fillcolor: "rgba(68, 68, 68, 0.1)",
            line: {color: "rgb(31, 119, 180)"},
            mode: "markers",
            name: "Measurement",
            type: "scatter"
        };

        var upperTrace = {
            x: x,
            y: upper,
            fill: "tonexty",
            fillcolor: "rgba(68, 68, 68, 0.1)",
            line: {width: 0},
            marker: {color: "444"},
            mode: "lines",
            name: "Upper Bound",
            type: "scatter"
        };

        return {
            data:[lowerTrace, middleTrace, upperTrace],
            layout:{
                showlegend: false
            }
        };
    }
    exports.makeContinuousLineData = makeContinuousLineData;

    /**
     *
     * @param dataSeries
     * @returns {{data: Array, layout: {showlegend: boolean}}}
     */
    function makeRangeData(dataSeries) {
        var data = [];
        dataSeries.forEach(function (series, trace_index) {
            if (series.outer && series.outer[0] < series.outer[1]) {
                data.push({
                  x: series.outer,
                  y: [series.index, series.index],
                  line: {
                      width: 3,
                      color: exports.getColor(trace_index, 0.4)
                  },
                  marker: {
                      width: 8,
                      color: exports.getColor(trace_index)
                  },
                  mode: "markers+lines",
                  name: series.name + ' Outer',
                  type: "scatter"
                });
            }

            if (series.inner && series.inner[0] < series.inner[1]) {
                data.push({
                  x: series.inner,
                  y: [series.index, series.index],
                  line: {
                      width: 10,
                      color: exports.getColor(trace_index)
                  },
                  mode: "lines",
                  name: series.name + ' Inner',
                  type: "scatter"
                });
            }

        });

        return {
            data:data,
            layout:{
                showlegend: false
            }
        };
    }
    exports.makeRangeData = makeRangeData;

    /**
     *
     * @param dataSeries
     * @param labels
     * @returns {*}
     */
    function makeBoxData(dataSeries, labels) {
        var data = dataSeries.map(function (data, index) {
            return {
                x: data,
                type: 'box',
                name: labels[index],
                boxpoints: false
            }
        });

        return {
            data: data,
            layout: {}
        };
    }
    exports.makeBoxData = makeBoxData;

    function makeOverlayHistogram(dataSeries, labels) {
        var data = dataSeries.map(function (data, index) {
            return {
                x: data,
                opacity: 0.5,
                type:'histogram',
                name: labels[index]
            };
        });

        return {
            data: data,
            layout: {
                barmode: 'overlay'
            }
        };
    }
    exports.makeOverlayHistogram = makeOverlayHistogram;

    /**
     *
     * @param title
     * @param xLabel
     * @param yLabel
     * @param args
     * @returns {*}
     */
    function makeLayout(args, title, xLabel, yLabel) {
        args = args || {};
        args.title = args.title || title;

        var font = {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        };

        var x = args.xaxis || {};
        x.title = x.title || xLabel;
        x.titlefont = x.titlefont || font;
        args.xaxis = x;

        var y = args.yaxis || {};
        y.title = y.title || yLabel;
        y.titlefont = y.titlefont || font;
        args.yaxis = y;

        return args;
    }
    exports.makeLayout = makeLayout;

}());
