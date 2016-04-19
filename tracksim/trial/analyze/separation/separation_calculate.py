from tracksim import limb


def lengths(foot_positions: limb.Property) -> dict:
    """

    :param foot_positions:
    :return:
    """

    left_lengths = []
    right_lengths = []

    for index in range(len(foot_positions.left_pes)):

        lp = foot_positions.left_pes[index]
        lm = foot_positions.left_manus[index]
        left_lengths.append(lp.distance_between(lm))

        rp = foot_positions.right_pes[index]
        rm = foot_positions.right_manus[index]
        right_lengths.append(rp.distance_between(rm))

    return dict(
        left_lengths=left_lengths,
        right_lengths=right_lengths
    )
