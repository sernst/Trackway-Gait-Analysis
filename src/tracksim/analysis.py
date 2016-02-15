
from tracksim import LimbProperty
from tracksim import number

def distance_between(p1, p2):
    """

    :param p1:
    :param p2:
    :return:
    """

    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if number.equivalent(dx.value, 0.0):
        sum_for_error = dx + dy
        return number.ValueUncertainty(
            abs(dy.raw),
            sum_for_error.raw_uncertainty)

    if number.equivalent(dy.value, 0.0):
        sum_for_error = dx + dy
        return number.ValueUncertainty(
            abs(dx.raw),
            sum_for_error.raw_uncertainty)

    try:
        return (
            dx ** 2 +
            dy ** 2) ** 0.5
    except Exception as err:
        print('Positions:', p1, p2, err)
        raise

def calculate_separations(foot_positions):
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

        left.append(distance_between(lp, lm))
        right.append(distance_between(rp, rm))
        front.append(distance_between(lm, rm))
        back.append(distance_between(lp, rp))

    return dict(
        left=left,
        right=right,
        front=front,
        back=back
    )

def calculate_gal(foot_positions):
    """

    :param foot_positions:
    :return:
    """

    out = []

    for i in range(len(foot_positions.values()[0])):

        pes_pos = get_midpoint(
            foot_positions.left_pes[i],
            foot_positions.right_pes[i])

        manus_pos = get_midpoint(
            foot_positions.left_manus[i],
            foot_positions.right_manus[i])

        out.append(distance_between(pes_pos, manus_pos))

    return out

def get_midpoint(position_a, position_b):
    """

    :param position_a:
    :param position_b:
    :return:
    """

    out = position_a.clone()
    out.x += 0.5*(position_b.x - position_a.x)
    out.y += 0.5*(position_b.y - position_a.y)
    return out

def calculate_plane_limb_extensions(foot_positions):
    """

    :param foot_positions:
    :return:
    """

    out = LimbProperty().assign([], [], [], [])

    for i in range(len(foot_positions.values()[0])):

        pes_pos = get_midpoint(
            foot_positions.left_pes[i],
            foot_positions.right_pes[i])

        for key in [LimbProperty.LEFT_PES, LimbProperty.RIGHT_PES]:
            out.get(key).append(distance_between(
                pes_pos,
                foot_positions.get(key)[i]
            ))

        manus_pos = get_midpoint(
            foot_positions.left_manus[i],
            foot_positions.right_manus[i])

        for key in [LimbProperty.LEFT_MANUS, LimbProperty.RIGHT_MANUS]:
            out.get(key).append(distance_between(
                manus_pos,
                foot_positions.get(key)[i]
            ))

    return out
