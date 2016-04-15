import plotly
import plotly.graph_objs as go

import tracksim
from tracksim import analysis

LIMB_PHASE = 90
PRINT_INTERVAL = 0

trial_info = analysis.cacher.fetch('trial_info')
results = analysis.cacher.fetch('results')

df = trial_info.query(
        'phase == {} and print_interval == {} and size_id == "S"'
        .format(LIMB_PHASE, PRINT_INTERVAL)
) .sort_values(by='duty_cycle')

traces = []

for index, row in df.iterrows():
    d = results['trials'][index]
    distribution = d['group']['couplings']['densities']['series'][
        row['trial_index']]
    traces.append(go.Scatter(
        name='DC {}'.format(row['duty_cycle']),
        x=d['group']['couplings']['densities']['x'],
        y=distribution
    ))

path = analysis.make_results_path('coupling_vs_duty_cycle.html')

plotly.offline.plot(
    {
        'data': traces,
        'layout': go.Layout(
            title='Coupling Density Distributions for Phase {}% and Print Interval {}'.format(
                LIMB_PHASE, PRINT_INTERVAL),
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
Coupling vs Duty Cycle Plot:
 * file://{}
""".format(path))
