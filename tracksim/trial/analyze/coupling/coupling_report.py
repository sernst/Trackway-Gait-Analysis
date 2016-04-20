import plotly.graph_objs as go

from tracksim.reporting import Report
from tracksim.reporting import plotting
import measurement_stats as mstats


def plot_lengths(
        report: Report,
        coupling_data: dict,
        times: dict
):
    """

    :param report:
    :param coupling_data:
    :param times:
    :return:
    """

    values, uncertainties = mstats.values.unzip(coupling_data['lengths'])

    plot = plotting.make_line_data(
        times['cycles'],
        values,
        uncertainties
    )

    report.add_plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            'Coupling Lengths',
            'Cycle (#)',
            'Length (m)'
        )
    )


def plot_distribution(report: Report, coupling_data: dict):
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


def plot_advance(report: Report, coupling_data: dict, times: dict):
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

        values, uncertainties = mstats.values.unzip(coupling_data[key])

        plot = plotting.make_line_data(
            x=times['cycles'],
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
            x_label='Cycle (#)',
            y_label='Advance Rate (m/cycle)'
        )
    )
