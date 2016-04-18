import plotly.graph_objs as go

from tracksim.analysis import report
from tracksim.analysis import shared

report.add_header(2, 'Coupling Range Comparisons')
report.add_plaintext("""
    The following plots show the relationships between coupling
    distance and print interval for a specified limb phase.

    Each plot consists of 3 groups of 4 line graphs. The 3 groups represent
    short, medium and long coupling distances for the given simulation as
    defined by increasing the spacing between the manus and pes coupling
    during simulation.

    Within each of the 3 groups are 4 line graphs, which represent the
    coupling range boundaries (+/- 2 standard deviations) for two different
    duty cycles (50% and 75%).
""")

couplings = shared.couplings


def add_to_plot(name, data_frame, lower_color, upper_color):
    data_frame = data_frame.sort_values(by='print_interval')
    x = data_frame['print_interval']
    out = []
    entries = [
        {
            'key': 'lower_2s', 'suffix': '-2s', 'line': True,
            'size': 9, 'alpha': 0.4,
            'color': lower_color
        },
        {
            'key': 'upper_2s', 'suffix': '+2s', 'line': True,
            'size': 9, 'alpha': 0.4,
            'color': upper_color
        }
    ]

    for e in entries:
        trace = go.Scatter(
            x=x,
            y=data_frame[e['key']],
            name='{} {}'.format(name, e['suffix']),
            mode='markers',
            marker=dict(
                size=e['size'],
                color=e['color'],
                opacity=e['alpha'],
                line=dict(width=1, color=e['color'])
            )
        )

        if e['line']:
            trace['mode'] = 'lines+markers'
            trace['line'] = dict(
                width=1,
                color=e['color']
            )
        out.append(trace)

    return out


def create_plot(limb_phase):

    data = []

    for size in ['short', 'medium', 'long']:

        data += add_to_plot(
            '{size} DC 0.5'.format(size=size.capitalize()),
            lower_color='blue',
            upper_color='red',
            data_frame=couplings.query("""
                phase == {limb_phase} and
                duty_cycle == 0.5 and
                size == "{size}"
            """.format(
                limb_phase=limb_phase,
                size=size
            ).replace('\n', ' '))
        )

        data += add_to_plot(
            '{size} DC 0.75'.format(size=size.capitalize()),
            upper_color='orange',
            lower_color='green',
            data_frame=couplings.query("""
                phase == {limb_phase} and
                duty_cycle == 0.75 and
                size == "{size}"
            """.format(
                limb_phase=limb_phase,
                size=size
            ).replace('\n', ' '))
        )

    layout = go.Layout(
        title='Coupling Ranges for Limb Phase {}%'.format(limb_phase),
        height=600,
        xaxis={
            'title': 'Print Interval (%)'
        },
        yaxis={
            'title': 'Coupling Distance (m)'
        }
    )

    report.add_plotly(data, layout)


create_plot(0)
create_plot(90)
create_plot(180)
create_plot(270)
