import measurement_stats as mstats
from measurement_stats import density

from tracksim import limb
from tracksim import trackway


def separations(foot_positions):
    """

    :param foot_positions:
    :return:
    """

    left = []
    right = []
    front = []
    back = []

    for i in range(len(foot_positions.values()[0])):
        lp = foot_positions.left_pes[i]
        rp = foot_positions.right_pes[i]
        lm = foot_positions.left_manus[i]
        rm = foot_positions.right_manus[i]

        left.append(lp.distance_between(lm))
        right.append(rp.distance_between(rm))
        front.append(lm.distance_between(rm))
        back.append(lp.distance_between(rp))

    return dict(
        left=left,
        right=right,
        front=front,
        back=back
    )


def coupling_distance(foot_positions):
    """

    :param foot_positions:
    :return:
    """

    data = []

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
        data.append(length)

    d = density.create_distribution(data)
    bounds = mstats.density.boundaries.weighted_two(d)
    median = bounds[2]
    mad = mstats.density.ops.weighted_median_average_deviation(d)
    deviations = mstats.values.deviations(median, data)

    min_value = d.minimum_boundary(3)
    max_value = d.maximum_boundary(3)

    x_values = mstats.ops.linear_space(min_value, max_value, 250)

    return dict(
        data=data,
        value=mstats.value.ValueUncertainty(median, mad),
        deviation_max=mstats.value.round_to_order(max(deviations), -2),
        bounds=bounds,
        distribution_profile={
            'x': x_values,
            'y': d.probabilities_at(x_values)
        },
        population=mstats.density.ops.population(d, 256)
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


def plane_limb_extensions(foot_positions):
    """

    :param foot_positions:
    :return:
    """

    out = limb.Property().assign([], [], [], [])

    for i in range(len(foot_positions.values()[0])):

        pes_pos = get_midpoint(
            foot_positions.left_pes[i],
            foot_positions.right_pes[i])

        for key in [limb.LEFT_PES, limb.RIGHT_PES]:
            out.get(key).append(pes_pos.distance_between(
                foot_positions.get(key)[i]
            ))

        manus_pos = get_midpoint(
            foot_positions.left_manus[i],
            foot_positions.right_manus[i])

        for key in [limb.LEFT_MANUS, limb.RIGHT_MANUS]:
            out.get(key).append(manus_pos.distance_between(
                foot_positions.get(key)[i]
            ))

    return out

