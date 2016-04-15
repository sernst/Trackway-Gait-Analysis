import plotly
import plotly.graph_objs as go

import tracksim
from tracksim import analysis


LIMB_PHASE = 90

couplings = analysis.cacher.fetch('couplings')


def add_to_plot(name, data_frame, lower_color, upper_color):
    data_frame = data_frame.sort_values(by='print_interval')
    x = data_frame['print_interval']
    out = []
    entries = [
        {'key': 'lower_2s', 'suffix': '-2s', 'size': 9, 'alpha': 0.4,
         'color': lower_color},
        {'key': 'lower_1s', 'suffix': '-1s', 'size': 6, 'alpha': 0.6,
         'color': lower_color},
        {'key': 'upper_1s', 'suffix': '+1s', 'size': 6, 'alpha': 0.6,
         'color': upper_color},
        {'key': 'upper_2s', 'suffix': '+2s', 'size': 9, 'alpha': 0.4,
         'color': upper_color}
    ]

    for e in entries:
        out.append(go.Scatter(
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
        ))
    return out


data = add_to_plot(
    'DC 0.5',
    couplings.query('phase == {} and duty_cycle == 0.5'.format(LIMB_PHASE)),
    'blue',
    'red'
)
data += add_to_plot(
    'DC 0.75',
    couplings.query('phase == {} and duty_cycle == 0.75'.format(LIMB_PHASE)),
    'green',
    'orange'
)

path = analysis.make_results_path('Coupling-Ranges.html')

plotly.offline.plot(
    {
        'data': data,
        "layout": go.Layout(
            title='Coupling Ranges for Limb Phase {}%'.format(LIMB_PHASE),
            height=600,
            xaxis={
                'title': 'Print Interval (%)'
            },
            yaxis={
                'title': 'Coupling Distance (m)'
            }
        )
    },
    filename=path,
    auto_open=False
)

tracksim.log("""
Coupling Range Plot:
 * file://{}
""".format(path))
