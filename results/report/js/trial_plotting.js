(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    var _elements;

    /**
     *
     * @returns {Element}
     */
    function createElement() {

        var plotElement = document.createElement('div');
        var container = document.getElementById('plotBox');

        plotElement.className = 'plot';
        container.appendChild(plotElement);
        _elements.push(plotElement);
        return plotElement;
    }

    /**
     *
     * @param x
     * @param y
     * @param yUnc
     * @returns {*[]}
     */
    function makeScatterData(x, y, yUnc) {
        return [{
            x: x,
            y: y,
            error_y: { type: 'data', array: yUnc, visible: true },
            type: 'scatter'
          }
        ];
    }

    /**
     *
     * @param title
     * @param xLabel
     * @param yLabel
     * @returns {*}
     */
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

    /**
     *
     */
    function makeGalPlot() {
        Plotly.newPlot(
            createElement(),
            makeScatterData(
                exports.DATA.time.progress,
                exports.DATA.gals.values,
                exports.DATA.gals.uncertainties),
            makeLayout(
                'Calculated Glenoacetabular Lengths',
                'Progress (%)',
                'Length (m)'
            )
        );
    }

    /**
     *
     */
    function makeSeparationPlots() {
        var entries = {
            left:['Left', 'Pes-Manus'],
            right:['Right', 'Pes-Manus'],
            front:['Front', 'Manus-Manus'],
            back:['Front', 'Pes-Pes']
        };

        Object.keys(entries).forEach(function (key) {
            var entry = entries[key];

            Plotly.newPlot(
                createElement(),
                makeScatterData(
                    exports.DATA.time.progress,
                    exports.DATA.separations[key].values,
                    exports.DATA.separations[key].uncertainties),
                makeLayout(
                    entry[0] + ' ' + entry[1] + ' Separation Distances',
                    'Progress (%)',
                    'Distance (m)'
                )
            );
        });
    }

    /**
     *
     */
    function makeExtensionPlots() {
        var entries = {
            left_pes:'Left Pes',
            right_pes:'Right Pes',
            left_manus:'Left Manus',
            right_manus:'Right Manus'
        };

        Object.keys(entries).forEach(function (key) {
            Plotly.newPlot(
                createElement(),
                makeScatterData(
                    exports.DATA.time.progress,
                    exports.DATA.extensions[key].values,
                    exports.DATA.extensions[key].uncertainties),
                makeLayout(
                    entries[key] + ' Extension Distances',
                    'Progress (%)',
                    'Distance (m)'
                )
            );
        });
    }

    /**
     *
     */
    function createPlots() {
        _elements = [];

        makeGalPlot();
        makeSeparationPlots();
        makeExtensionPlots();

        window.onresize = function() {
            _elements.forEach(function(e) {
                Plotly.Plots.resize(e);
            });
        };
    }
    exports.createPlots = createPlots;

}());
