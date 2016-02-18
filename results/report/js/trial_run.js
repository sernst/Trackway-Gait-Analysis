(function () {
    'use strict';

    var exports = window.SIM || {};
    window.SIM = exports;

    function onData(data) {
        exports.DATA = data;

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

    /**
     * RUN APPLICATION
     */
    $(function () {
        exports.PARAMS = {};
        document.location.search
            .replace(/(^\?)/,'')
            .split("&")
            .forEach(function (item) {
                item = item.split("=");
                if (item.length < 2) { return; }

                var v = item[1];
                if (!/[^0-9\.]+/.test(v)) {
                  if (v.indexOf('.') === -1) {
                    v = parseInt(v, 10);
                  } else {
                    v = parseFloat(v);
                  }
                } else if (v.toLowerCase() === 'true') {
                  v = true;
                } else if (v.toLowerCase() === 'false') {
                  v = false;
                } else {
                  v = decodeURIComponent(v);
                }

                exports.PARAMS[item[0]] = v;
            });

        var urlRoot = 'trials/' + exports.PARAMS['trial'] + '/' +
                exports.PARAMS['trial'];

        $('.svg-box').load(urlRoot + '.svg', function () {
            $.getJSON(urlRoot + '.json', onData);
        });
    });

}());
