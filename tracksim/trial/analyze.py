import measurement_stats as mstats

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

    two_sigma_bounds = [-1e6, 1e6]
    one_sigma_bounds = [-1e6, 1e6]
    bounds_list = []

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

        bounds = (
            length.value - 2.0 * length.uncertainty,
            length.value - length.uncertainty,
            length.value,
            length.value + length.uncertainty,
            length.value + 2.0 * length.uncertainty
        )
        bounds_list.append(bounds)

        one_sigma_bounds = [
            max(one_sigma_bounds[0], bounds[1]),
            min(one_sigma_bounds[1], bounds[3])
        ]

        two_sigma_bounds = [
            max(two_sigma_bounds[0], bounds[0]),
            min(two_sigma_bounds[1], bounds[4])
        ]
        data.append(length)

    mean = mstats.mean.weighted_mean_and_deviation(*data)
    deviations = mstats.values.deviations(mean.value, data)

    return dict(
        data=data,
        value=mean,
        deviation_max=mstats.value.round_to_order(max(deviations), -2),
        bounds=dict(
            one_sigma=one_sigma_bounds,
            two_sigma=two_sigma_bounds
        ),
        bounds_list=bounds_list
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

