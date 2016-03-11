(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     *
     */
    function onData(data) {
        exports.DATA = data;

        $('.group-info .title').html(data.configs.name);
        $('.group-info .summary').html(data.configs.summary);
        $('.group-info .date').html(data.date);
        $('title').html(data.configs.name);
        exports.addTrialListings(data.trials);

        exports.makeCouplingPlot();
    }
    exports.onData = onData;

    /**
     *
     */
    function run() {
        var dataFilename = 'groups/' + exports.PARAMS['id'] + '/' +
                exports.PARAMS['id'] + '.js';
        exports.loadDataFile('SIM_DATA', dataFilename);
    }
    exports.run = run;

}());
