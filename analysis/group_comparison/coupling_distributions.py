import plotly
import plotly.graph_objs as go

from tracksim.analysis import report
from tracksim.analysis import shared

LIMB_PHASE = 90
DUTY_CYCLE = 0.8

results = shared.results
trial_info = shared.trial_info

df = trial_info.query(
    'phase == {lp} and duty_cycle == {dc} and size_id == "S"'.format(
        lp=LIMB_PHASE,
        dc=DUTY_CYCLE)
).sort_values(by='print_interval')

traces = []

for index, row in df.iterrows():
    d = results['trials'][index]
    distribution = d['group']['couplings']['densities']['series'][
        row['trial_index']]
    traces.append(go.Scatter(
        name='PI {print_interval}%'.format(
            print_interval=row['print_interval']),
        x=d['group']['couplings']['densities']['x'],
        y=distribution
    ))

report.add_html(plotly.offline.plot({
        'data': traces,
        'layout': go.Layout(
            title='Coupling Density Distributions for Phase {}% and DC {}'.format(
                LIMB_PHASE, DUTY_CYCLE),
            height=600,
            xaxis={
                'title': 'Coupling Distance (m)'
            },
            yaxis={
                'title': 'Probability Density (au)'
            }
        )
    },
    output_type='div',
    include_plotlyjs=False
))

