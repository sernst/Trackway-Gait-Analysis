(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     * Called by the trial listings at the top of the page when clicked, which
     * opens the specified trial results page for that trial in a new browser
     * window/tab.
     *
     * @param trialId
     *  The uid of the trial to be opened
     */
    function onTrialClick(trialId) {
        window.open(
            'trial.html?id=' + encodeURIComponent(trialId),
            '_blank'
        );
    }
    exports.onTrialClick = onTrialClick;

    /**
     * Called when the page has finished loading and is ready to run
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
