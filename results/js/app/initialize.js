(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    exports.resizeCallbacks = [];

    /**
     * A fake require function that is needed for the inclusion of some
     * elements within the DOM (e.g. plotly offline)
     *
     * @param preloaders
     * @param callback
     */
    function fakeRequire(preloaders, callback) {
        var callers = [];
        preloaders.forEach(function (entry) {
            if (entry === 'plotly') {
                callers.push(window.Plotly);
            }
        });
        callback.apply(this, callers);
    }
    window.require = fakeRequire;

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
    exports.toDisplayNumber = toDisplayNumber;

    /**
     * @param filename
     */
    function loadDataFile(filename) {
        return new Promise(function (resolve) {

            function loadComplete() {
                exports.DATA = window.SIM_DATA.data;
                $('.body-wrapper').html(window.SIM_DATA.body);
                resolve(exports.DATA);
                $(window).trigger('resize');
            }

            var script = document.createElement('script');
            script.onload = loadComplete;
            script.src = filename;
            document.head.appendChild(script);
        });
    }
    exports.loadDataFile = loadDataFile;

}());
