(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    function getIndexes(values) {
        return values.map(function (value, index) {
            return index + 1;
        });
    }

    /**
     *
     */
    function makeCouplingPlot() {
        var couplings = exports.DATA.couplings;

        var plot = exports.plot.makeBoxData(
            couplings.populations,
            getIndexes(couplings.populations)
        );
        plot.layout.showlegend = false;

        Plotly.newPlot(
            exports.plot.createElement('#plotBox'),
            plot.data,
            exports.plot.makeLayout(
                plot.layout,
                'Coupling Lengths',
                'Length (m)',
                'Trial (#)'
            )
        );

        var dataSeries = couplings.densities.series.map(function (item, index) {
            return {
                x: couplings.densities.x,
                y: item,
                name: index + 1
            };
        });
        plot = exports.plot.makeLines(dataSeries);

        Plotly.newPlot(
            exports.plot.createElement('#plotBox'),
            plot.data,
            exports.plot.makeLayout(
                plot.layout,
                'Coupling Length Distributions',
                'Length (m)',
                'Expectation (AU)'
            )
        );

        dataSeries = couplings.bounds.map(function (item, index) {
            return {
                inner: [item[1], item[3]],
                outer: [item[0], item[4]],
                index: index + 1,
                name: index + 1
            };
        });
        plot = exports.plot.makeRangeData(dataSeries);

        Plotly.newPlot(
            exports.plot.createElement('#plotBox'),
            plot.data,
            exports.plot.makeLayout(
                plot.layout,
                'Coupling Length IQR Ranges',
                'Length (m)',
                'Trial (#)'
            )
        );
    }
    exports.makeCouplingPlot = makeCouplingPlot;

}());
