(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     *
     */
    function run() {
        var dataFilename = 'reports/analysis/' +
            exports.PARAMS['id'] + '/' +
            exports.PARAMS['id'] + '.js';

        return exports.loadDataFile(dataFilename)
            .then(function () {
                $('title').html(data.settings.title || 'Analysis');
            });
    }

    exports.run = run;

}());


