(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     *
     * @param data
     */
    function onData(data) {
        exports.DATA = data;

        $('.svg-box').html(data.svg);

        var controlBar = $('.playback-controls');

        $('.header-title').html(data.configs.name);
        $('title').html(data.configs.name);
        $('.header-summary').html(data.configs.summary);
        $('.header-entry.date .value').html(data.date);
        $('.header-entry.duty-cycle .value').html(
            Math.round(100.0*data.configs.duty_cycle)
        );

        var box = $('.header-entry.limb-phases .value');
        Object.keys(data.limb_phases).forEach(function (limbId) {
            box.find('.' + limbId + '-value').html(
                Math.round(100.0*data.limb_phases[limbId]) + '%'
            );
        });

        exports.initializeResultsDisplay();
        exports.createPlots();

        controlBar.find('.control').click(function (event) {
            exports.onPlaybackControl($(event.currentTarget).attr('data-role'));
        });
        controlBar.find('.play-icon').hide();

        exports.populateCycleDisplay();
        exports.onPlaybackControl('toggle-play');

        $('#displayWrapper').show();
        $(window).trigger('resize');
    }
    exports.onData = onData;

    /**
     * RUN APPLICATION
     */
    function run() {
        var filename = 'trials/' + exports.PARAMS['id'] + '/' +
                exports.PARAMS['id'] + '.js';
        exports.loadDataFile('SIM_DATA', filename);
    }
    exports.run = run;

}());
