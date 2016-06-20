import plotly.graph_objs as go

from tracksim.reporting import Report
from tracksim.reporting import plotting
import measurement_stats as mstats


def plot_lengths(
        report: Report,
        coupling_data: dict
):
    """

    :param report:
    :param coupling_data:
    :param times:
    :param sampled:
    :return:
    """

    times = [e.time for e in coupling_data['lengths']]
    lengths = [e.value for e in coupling_data['lengths']]
    values, uncertainties = mstats.values.unzip(lengths)

    plot = plotting.make_line_data(
        times,
        values,
        uncertainties,
        name='Length'
    )

    report.add_plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            'Coupling Lengths',
            'Activity Cycle (#)',
            'Length (m)'
        )
    )


def plot_deviations(
        report: Report,
        coupling_data: dict
):
    """

    :param report:
    :param coupling_data:
    :return:
    """

    times = [e.time for e in coupling_data['lengths']]
    deviations = []
    for dev in coupling_data['deviations']:
        deviations.append(100.0 * dev)

    values, uncertainties = mstats.values.unzip(deviations)

    plot = plotting.make_line_data(
        times,
        values,
        uncertainties,
        name='Deviation',
        color=plotting.get_color(1, as_string=True)
    )

    report.add_plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            'Coupling Length Median Deviations',
            'Activity Cycle (#)',
            'Median Deviation (%)'
        )
    )


def plot_distribution(
        report: Report,
        coupling_data: dict
):
    """

    :param report:
    :param coupling_data:
    :return:
    """

    report.add_plotly(
        data=[go.Scatter(
            x=coupling_data['distribution_profile']['x'],
            y=coupling_data['distribution_profile']['y'],
            mode='lines'
        )],
        layout=plotting.create_layout(
            title='Coupling Length Distribution',
            x_label='Coupling Distance (m)',
            y_label='Expectation (au)'
        )
    )


def plot_advance(report: Report, coupling_data: dict):
    """

    :param report:
    :param coupling_data:
    :param times:
    :return:
    """

    traces = []

    sources = dict(
        rear_advance={
            'name': 'Rear',
            'index': 0
        },
        forward_advance={
            'name': 'Forward',
            'index': 1
        }
    )

    for key, data in sources.items():
        events = coupling_data[key]

        times = [e.time for e in events]
        values, uncertainties = mstats.values.unzip([e.value for e in events])

        plot = plotting.make_line_data(
            x=times,
            y=values,
            y_unc=uncertainties,
            name=data['name'],
            color=plotting.get_color(data['index'], 0.6, as_string=True),
            fill_color=plotting.get_color(data['index'], 0.2, as_string=True)
        )
        traces += plot['data']

    report.add_plotly(
        data=traces,
        layout=plotting.create_layout(
            title='Coupler Rate of Advancement',
            x_label='Activity Cycle (#)',
            y_label='Advance Rate (m/cycle)'
        )
    )
