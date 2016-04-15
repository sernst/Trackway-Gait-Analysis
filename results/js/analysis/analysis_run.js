window.require = function (preloaders, callback) {
    var callers = [];
    preloaders.forEach(function (entry) {
        if (entry === 'plotly') {
            callers.push(window.Plotly);
        }
    });
    callback.apply(this, callers);
};
