import typing

import measurement_stats as mstats
from measurement_stats.distributions import boxes

from tracksim import limb


def positions(foot_positions: limb.Property) -> typing.Dict[str, list]:
    """
    Iterates over the foot positions lists and computes the coupling length for
    each entry in the lists (a time step of the simulation) as well as the
    positions of the rear and forward couplers.

    :param foot_positions:
        The foot positions for each limb at each simulated time step

    :return:
        A dictionary with the following keys:
            * lengths: The coupling length at each simulated time step
            * rear: The rear coupler position at each simulated time step
            * forward: The forward coupler position at each simulated time step
    """
    coupling_lengths = []
    pes_coupler_positions = []
    manus_coupler_positions = []

    for i in range(len(foot_positions.values()[0])):
        pes_pos = foot_positions.left_pes[i].midpoint_between(
            foot_positions.right_pes[i]
        )
        pes_coupler_positions.append(pes_pos)

        manus_pos = foot_positions.left_manus[i].midpoint_between(
            foot_positions.right_manus[i]
        )
        manus_coupler_positions.append(manus_pos)

        coupling_lengths.append(pes_pos.distance_between(manus_pos))

    return dict(
        lengths=coupling_lengths,
        rear=pes_coupler_positions,
        forward=manus_coupler_positions
    )


def statistics(coupling_positions: typing.Dict[str, list]) -> dict:
    """

    :param coupling_positions:
    :return:
    """

    d = mstats.create_distribution(coupling_positions['lengths'])
    bounds = boxes.weighted_two(d)
    median = bounds[2]
    mad = mstats.distributions.weighted_median_average_deviation(d)

    min_value = d.minimum_boundary(3)
    max_value = d.maximum_boundary(3)

    x_values = mstats.ops.linear_space(min_value, max_value, 250)

    return dict(
        value=mstats.value.ValueUncertainty(median, mad),
        bounds=bounds,
        distribution_profile={
            'x': x_values,
            'y': d.probabilities_at(x_values)
        },
        population=mstats.distributions.population(d, 256),
    )


def advance(
        coupling_positions: typing.Dict[str, list]
) -> typing.Dict[str, typing.List[mstats.ValueUncertainty]]:
    """

    :param coupling_positions:
    :return:
    """

    rear = coupling_positions['rear']
    fore = coupling_positions['forward']

    rear_advance = []
    fore_advance = []

    for i in range(1, len(rear) - 1):

        rear_advance.append(
            0.5 * rear[i + 1].distance_between(rear[i - 1])
        )

        fore_advance.append(
            0.5 * fore[i + 1].distance_between(fore[i - 1])
        )

    rear_advance.insert(0, rear_advance[0].clone())
    rear_advance.append(rear_advance[-1].clone())

    fore_advance.insert(0, fore_advance[0].clone())
    fore_advance.append(fore_advance[-1].clone())

    return dict(
        rear_advance=rear_advance,
        forward_advance=fore_advance
    )
