(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    /**
     * RUN APPLICATION
     */
    function run() {
        var filename = 'reports/trial/' +
            exports.PARAMS['id'] + '/' +
            exports.PARAMS['id'] + '.js';

        return exports.loadDataFile(filename)
            .then(function (data) {

                $('title').html($('.header-title').html());

                var controlBar = $('.playback-controls');
                controlBar.find('.control').click(function (event) {
                    exports.onPlaybackControl(
                        $(event.currentTarget).attr('data-role')
                    );
                });
                controlBar.find('.play-icon').hide();

                exports.drawMidline();
                exports.initialize_animation();
                exports.populateCycleDisplay();
                exports.onPlaybackControl('toggle-play');
            });
    }
    exports.run = run;

}());
