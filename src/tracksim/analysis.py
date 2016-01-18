
import math

def calculate_extensions(foot_positions):
    """

    :param foot_positions:
    :return:
    """

    left = []
    right = []
    front = []
    back = []

    def get_distance(p1, p2):
        try:
            return (
                (p2.x - p1.x) ** 2 +
                (p2.y - p1.y) ** 2) ** 0.5
        except Exception as err:
            print('Positions:', p1, p2)
            raise

    for i in range(len(foot_positions.values()[0])):
        lp = foot_positions.left_pes[i]
        rp = foot_positions.right_pes[i]
        lm = foot_positions.left_manus[i]
        rm = foot_positions.right_manus[i]

        left.append(get_distance(lp, lm))
        right.append(get_distance(rp, rm))
        front.append(get_distance(lm, rm))
        back.append(get_distance(lp, rp))

    return dict(
        left=left,
        right=right,
        front=front,
        back=back )

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

        out.append((
            (pes_pos.x - manus_pos.x) ** 2 +
            (pes_pos.y - manus_pos.y) ** 2) ** 0.5)

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

