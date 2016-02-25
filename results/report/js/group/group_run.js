(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    function onData(data) {
        exports.DATA = data;

        $('.group-info .title').html(data.configs.name);
        $('.group-info .summary').html(data.configs.summary);
        $('.group-info .date').html(data.date);
        $('title').html(data.configs.name);
        exports.addTrialListings(data.trials);

        exports.makeCouplingPlot();
    }

    function run() {
        var urlRoot = 'groups/' + exports.PARAMS['id'] + '/' +
                exports.PARAMS['id'];

        $.getJSON(urlRoot + '.json')
            .then(function (data) {
                onData(data);
                $(window).trigger('resize');
            })
    }
    exports.run = run;

}());
