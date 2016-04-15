(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     *
     */
    function makeCouplingPlot() {
        var plot = exports.plot.makeContinuousLineData(
            exports.DATA.time.progress,
            exports.DATA.couplings.values,
            exports.DATA.couplings.uncertainties
        );

        Plotly.newPlot(
            exports.plot.createElement('#plotBox'),
            plot.data,
            exports.plot.makeLayout(
                plot.layout,
                'Calculated Coupling Lengths',
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
            var plot = exports.plot.makeContinuousLineData(
                exports.DATA.time.progress,
                exports.DATA.separations[key].values,
                exports.DATA.separations[key].uncertainties
            );

            Plotly.newPlot(
                exports.plot.createElement('#plotBox'),
                plot.data,
                exports.plot.makeLayout(
                    plot.layout,
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
            var plot = exports.plot.makeContinuousLineData(
                exports.DATA.time.progress,
                exports.DATA.extensions[key].values,
                exports.DATA.extensions[key].uncertainties
            );

            Plotly.newPlot(
                exports.plot.createElement('#plotBox'),
                plot.data,
                exports.plot.makeLayout(
                    plot.layout,
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
        makeCouplingPlot();
        makeSeparationPlots();
        makeExtensionPlots();
    }
    exports.createPlots = createPlots;

}());
