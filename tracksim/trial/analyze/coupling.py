import typing

import plotly.graph_objs as go

import measurement_stats as mstats
from measurement_stats.density import boundaries

from tracksim import trackway
from tracksim import limb
from tracksim.reporting import Report
from tracksim.reporting import plotting


def calculate(foot_positions: limb.Property) -> dict:
    """

    :param foot_positions:
    :return:
    """

    couplings = []

    for i in range(len(foot_positions.values()[0])):
        pes_pos = get_midpoint(
            foot_positions.left_pes[i],
            foot_positions.right_pes[i]
        )

        manus_pos = get_midpoint(
            foot_positions.left_manus[i],
            foot_positions.right_manus[i]
        )

        length = pes_pos.distance_between(manus_pos)
        couplings.append(length)

    d = mstats.density.create_distribution(couplings)
    bounds = boundaries.weighted_two(d)
    median = bounds[2]
    mad = mstats.density.ops.weighted_median_average_deviation(d)

    min_value = d.minimum_boundary(3)
    max_value = d.maximum_boundary(3)

    x_values = mstats.ops.linear_space(min_value, max_value, 250)

    return dict(
        couplings=couplings,
        value=mstats.value.ValueUncertainty(median, mad),
        bounds=bounds,
        distribution_profile={
            'x': x_values,
            'y': d.probabilities_at(x_values)
        },
        population=mstats.density.ops.population(d, 256)
    )


def serialize(coupling_data: dict) -> dict:
    """

    :param coupling_data:
    :return:
    """

    out = dict(**coupling_data)

    couplings = []
    for value in coupling_data['couplings']:
        couplings.append(value.serialize())

    out['couplings'] = couplings
    out['value'] = coupling_data['value'].serialize()

    return out


def add_to_report(
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

    values, uncertainties = mstats.values.unzip(coupling_data['couplings'])

    plot = plotting.make_line_data(
        times['progress'],
        values,
        uncertainties
    )

    report.add_plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            'Coupling Length',
            'Progress (%)',
            'Length (m)'
        )
    )

    report.add_plotly(
        data=[go.Scatter(
            x=coupling_data['distribution_profile']['x'],
            y=coupling_data['distribution_profile']['y'],
            mode='lines'
        )],
        layout=plotting.create_layout(
            title='Coupling Length Distribution',
            x_label='Coupling Distance (m)',
            y_label='Normalized Probability Density (au)'
        )
    )


def get_midpoint(position_a, position_b):
    """

    :param position_a:
    :param position_b:
    :return:
    """

    return trackway.TrackPosition(
        x=0.5 * (position_a.x + position_b.x),
        y=0.5 * (position_a.y + position_b.y)
    )

