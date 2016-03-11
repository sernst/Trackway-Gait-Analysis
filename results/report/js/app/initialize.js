(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    exports.resizeCallbacks = [];

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
     * @param key
     * @param filename
     */
    function loadDataFile(key, filename) {
        var script = document.createElement('script');
        script.setAttribute('onload', 'window.SIM.onData(window.' + key + ')');
        script.setAttribute('src', filename);
        document.head.appendChild(script);
    }
    exports.loadDataFile = loadDataFile;

}());
