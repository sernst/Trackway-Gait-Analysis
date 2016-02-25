(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     *
     * @param trials
     */
    function addTrialListings(trials) {
        trials.forEach(function (trialData) {
           addListing(trialData);
        })
    }
    exports.addTrialListings = addTrialListings;

    /**
     *
     * @param trialData
     */
    function addListing(trialData) {

        var e = $('<div></div>')
            .addClass('entry')
            .appendTo($('.trial-listings'));

        $('<div></div>')
            .addClass('title')
            .html(trialData.index + '. ' + trialData.name)
            .appendTo(e);

        $('<div></div>')
            .addClass('summary')
            .html(trialData.summary)
            .appendTo(e);

        e.click(function () {
            window.open(
                'trial.html?id=' + encodeURIComponent(trialData.id),
                '_blank'
            );
        });
    }
    exports.addTrialListings = addTrialListings;

}());
