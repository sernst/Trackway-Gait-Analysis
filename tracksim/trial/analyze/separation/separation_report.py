import measurement_stats as mstats

from tracksim.reporting import Report
from tracksim.reporting import plotting


def add_length_plot(report: Report, separation_data: dict, times:dict):
    """

    :param report:
    :param separation_data:
    :param times:
    :return:
    """

    sources = [
        dict(
            name='Left',
            data=separation_data['left_lengths'],
            index=2
        ),
        dict(
            name='Right',
            data=separation_data['right_lengths'],
            index=4
        )
    ]

    traces = []

    for source in sources:
        index = sources.index(source)
        values, uncertainties = mstats.values.unzip(source['data'])

        plot = plotting.make_line_data(
            x=times['cycles'],
            y=values,
            y_unc=uncertainties,
            name=source['name'],
            color=plotting.get_color(source['index'], 0.7, as_string=True),
            fill_color=plotting.get_color(source['index'], 0.2, as_string=True)
        )
        traces += plot['data']

    report.add_plotly(
        data=traces,
        layout=plotting.create_layout(
            title='Manus-Pes Separations',
            x_label='Cycle (#)',
            y_label='Separation (m)'
        )
    )
