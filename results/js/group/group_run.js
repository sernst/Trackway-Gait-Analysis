(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     *
     */
    function run() {
        var dataFilename = 'reports/group/' +
            exports.PARAMS['id'] + '/' +
            exports.PARAMS['id'] + '.js';

        return exports.loadDataFile(dataFilename)
            .then(function () {
                $('title').html($('.group-info .title').html());
            });
    }
    exports.run = run;

}());
