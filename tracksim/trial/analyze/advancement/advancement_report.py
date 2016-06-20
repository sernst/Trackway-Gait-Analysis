import measurement_stats as mstats

from tracksim.reporting import Report
from tracksim.reporting import plotting


def plot_strides(
        report: Report,
        advancement_data: dict
):
    """

    :param report:
    :param advancement_data:
    :return:
    """

    keys = (
        (0, 'left_pes_strides'),
        (1, 'right_pes_strides'),
        (2, 'left_manus_strides'),
        (4, 'right_manus_strides')
    )

    traces = []
    layout = dict()

    for entry in keys:
        color_index = entry[0]
        key = entry[1]


        times = [e.time for e in advancement_data[key]]
        values = [e.value for e in advancement_data[key]]
        values, uncertainties = mstats.values.unzip(values)

        name = ' '.join(key.split('_')[:2]).capitalize()
        plot = plotting.make_line_data(
            times,
            values,
            uncertainties,
            name=name,
            color=plotting.get_color(color_index, 0.5, True),
            fill_color=plotting.get_color(color_index, 0.2, True)
        )
        traces.extend(plot['data'])
        layout.update(plot['layout'])

    report.add_plotly(
        data=traces,
        layout=plotting.create_layout(
            layout,
            'Stepping Distances',
            'Activity Cycle (#)',
            'Distance (m)'
        )
    )
