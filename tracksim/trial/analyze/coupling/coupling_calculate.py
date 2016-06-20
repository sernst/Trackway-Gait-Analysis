import typing

import measurement_stats as mstats
from measurement_stats.distributions import boxes

from tracksim import limb
from tracksim import events


def positions(
        foot_positions: limb.Property,
        times: dict
) -> typing.Dict[str, list]:
    """
    Iterates over the foot positions lists and computes the coupling length for
    each entry in the lists (a time step of the simulation) as well as the
    positions of the rear and forward couplers.

    :param foot_positions:
        The foot positions for each limb at each simulated time step

    :param times:

    :return:
        A dictionary with the following keys:
            * lengths: The coupling length at each simulated time step
            * rear: The rear coupler position at each simulated time step
            * forward: The forward coupler position at each simulated time step
    """

    coupling_events = []
    pes_coupler_positions = []
    manus_coupler_positions = []
    midpoint_positions = []

    for i, time in enumerate(times['cycles']):
        pes_pos = foot_positions.left_pes[i].midpoint_between(
            foot_positions.right_pes[i]
        )
        pes_coupler_positions.append(pes_pos)

        manus_pos = foot_positions.left_manus[i].midpoint_between(
            foot_positions.right_manus[i]
        )
        manus_coupler_positions.append(manus_pos)

        midpoint_pos = pes_pos.midpoint_between(manus_pos)
        midpoint_positions.append(midpoint_pos)

        sample_time = 2 * time
        if not mstats.value.equivalent(sample_time - int(sample_time), 0):
            continue

        coupling_events.append(events.Event(
            time=time,
            index=i,
            value=pes_pos.distance_between(manus_pos)
        ))

    lengths = [v.value for v in coupling_events]
    d = mstats.create_distribution(lengths)
    median = mstats.distributions.percentile(d, 0.5)
    median_deviations = []

    for cl in lengths:
        median_deviations.append(cl - median)

    return dict(
        lengths=coupling_events,
        rear=pes_coupler_positions,
        forward=manus_coupler_positions,
        midpoints=midpoint_positions,
        deviations=median_deviations
    )


def statistics(coupling_positions: typing.Dict[str, list]) -> dict:
    """

    :param coupling_positions:
    :return:
    """

    lengths = coupling_positions['lengths']
    lengths = [e.value for e in lengths]

    d = mstats.create_distribution(lengths)
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
        foot_positions: limb.Property,
        coupling_positions: typing.Dict[str, list],
        times: dict
) -> typing.Dict[str, typing.List[mstats.ValueUncertainty]]:
    """

    :param foot_positions:
    :param coupling_positions:
    :param times:
    :return:
    """

    rear = coupling_positions['rear']
    fore = coupling_positions['forward']
    times = times['cycles']

    rear_advance = []
    fore_advance = []

    time_delta = times[1] - times[0]
    c = 0.5 / time_delta

    for i in range(1, len(times) - 1):
        time = times[i]

        moving = bool(
            (
                foot_positions.left_pes[i - 1].annotation != 'F' or
                foot_positions.right_pes[i - 1].annotation != 'F'
            ) and (
                foot_positions.left_pes[i + 1].annotation != 'F' or
                foot_positions.right_pes[i + 1].annotation != 'F'
            )
        )

        if moving:
            rear_advance.append(events.Event(
                time=time,
                index=i,
                value=c * rear[i + 1].distance_between(rear[i - 1])
            ))

        moving = bool(
            (
                foot_positions.left_manus[i - 1].annotation != 'F' or
                foot_positions.right_manus[i - 1].annotation != 'F'
            ) and (
                foot_positions.left_manus[i + 1].annotation != 'F' or
                foot_positions.right_manus[i + 1].annotation != 'F'
            )
        )

        if moving:
            fore_advance.append(events.Event(
                time=time,
                index=i,
                value=c * fore[i + 1].distance_between(fore[i - 1])
            ))

    return dict(
        rear_advance=rear_advance,
        forward_advance=fore_advance
    )
