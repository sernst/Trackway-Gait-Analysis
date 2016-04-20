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
            layout=plotting.create_layout(
                title='Left &amp; Right Separations',
                x_label='Cycle (#)',
                y_label='Separation (m)'
            ),
            items=[
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
        ),

        dict(
            layout=plotting.create_layout(
                title='Forward &amp; Rear Separations',
                x_label='Cycle (#)',
                y_label='Separation (m)'
            ),
            items=[
                dict(
                    name='Forward',
                    data=separation_data['forward_lengths'],
                    index=1
                ),
                dict(
                    name='Rear',
                    data=separation_data['rear_lengths'],
                    index=0
                )
            ]
        )
    ]

    for source in sources:
        traces = []

        for item in source['items']:
            values, uncertainties = mstats.values.unzip(item['data'])
            color = plotting.get_color(item['index'], 0.7, as_string=True)
            fill = plotting.get_color(item['index'], 0.2, as_string=True)

            plot = plotting.make_line_data(
                x=times['cycles'],
                y=values,
                y_unc=uncertainties,
                name=item['name'],
                color=color,
                fill_color=fill
            )
            traces += plot['data']

        report.add_plotly(data=traces, layout=source['layout'])
