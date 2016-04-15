import plotly
import plotly.graph_objs as go

import tracksim
from tracksim import analysis

LIMB_PHASE = 90
DUTY_CYCLE = 0.75

results = analysis.cacher.fetch('results')
trial_info = analysis.cacher.fetch('trial_info')

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

path = analysis.make_results_path('Coupling-Distributions.html')

plotly.offline.plot({
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
    filename=path,
    auto_open=False
)

tracksim.log("""
Coupling Distribution Plot:
 * file://{}
""".format(path))
