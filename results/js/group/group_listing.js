(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    function onTrialClick(trialId) {
        window.open(
            'trial.html?id=' + encodeURIComponent(trialId),
            '_blank'
        );
    }
    exports.onTrialClick = onTrialClick;

}());
