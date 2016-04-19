import plotly.graph_objs as go

from tracksim.reporting import plotting
from tracksim.analysis import report
from tracksim.analysis import shared

report.add_header(2, 'Coupling Range Comparisons')

trial_info = shared.trial_info
couplings = shared.couplings


def add_to_plot(name, data_frame, color):
    data_frame = data_frame.sort_values(by='print_interval')

    data = []
    for index, row in data_frame.iterrows():
        coupling_data = couplings[row['id']]

        print_interval = row['print_interval']

        data.append(go.Box(
            name='PI {}%'.format(print_interval),
            y=coupling_data['population'],
            marker={'color': color},
            line=dict(
                outliercolor=color,
                outlierwidth=2,
            ),
            boxpoints=False
        ))

    return data


def create_plot(limb_phase):

    data = []

    for size in ['medium']:

        data += add_to_plot(
            'DC 0.5',
            color=plotting.get_color(0, 0.3, as_string=True),
            data_frame=trial_info.query("""
                phase == {limb_phase} and
                duty_cycle == 0.5 and
                size == "{size}"
            """.format(
                limb_phase=limb_phase,
                size=size
            ).replace('\n', ' '))
        )

        data += add_to_plot(
            'DC 0.8',
            color=plotting.get_color(1, 0.3, as_string=True),
            data_frame=trial_info.query("""
                phase == {limb_phase} and
                duty_cycle == 0.8 and
                size == "{size}"
            """.format(
                limb_phase=limb_phase,
                size=size
            ).replace('\n', ' '))
        )

    layout = go.Layout(
        title='Medium Coupling Ranges for Limb Phase {}%'.format(limb_phase),
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
