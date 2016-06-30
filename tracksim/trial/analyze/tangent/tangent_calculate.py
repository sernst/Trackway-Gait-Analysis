import typing

import measurement_stats as mstats

from tracksim import limb
from tracksim.trackway import TrackPosition
from tracksim.trial.analyze import geometry


def create_tangents(foot_positions: limb.Property) -> limb.Property:
    """

    :param foot_positions:
    :return:
    """

    def find_next_position(_positions, _i):
        reference_pos = _positions[_i]
        for pos in _positions[(i + 1):]:
            identical = (
                mstats.value.equivalent(pos.x.raw, reference_pos.x.raw, 0.1),
                mstats.value.equivalent(pos.y.raw, reference_pos.y.raw, 0.1)
            )
            if not identical[0] or not identical[1]:
                return pos
        return None

    tangents = limb.Property().assign([], [], [], [])

    for key in limb.KEYS:
        positions = foot_positions.get(key)

        for i in range(len(positions)):
            p = positions[i]
            next_pos = find_next_position(positions, i)

            if not next_pos or i >= (len(positions) - 1):
                try:
                    tan = tangents.get(key)[-1]
                except IndexError as err:
                    print('Index:', i)
                    print('Positions:', len(positions))
                    print('Next:', next_pos)
                    raise err
            else:
                tan = geometry.LineSegment2D(p, next_pos)
                tan.post_extend_line(4)
                tan.pre_extend_line(4)

            tangents.get(key).append(tan)

    return tangents


def compute_support_box(
        left_position: TrackPosition,
        left_tangent: geometry.LineSegment2D,
        right_position: TrackPosition,
        right_tangent: geometry.LineSegment2D,
        last_left_position: TrackPosition = None,
        next_left_position: TrackPosition = None
) -> typing.List:
    """

    :param left_position:
    :param left_tangent:
    :param right_position:
    :param right_tangent:
    :param last_left_position:
    :param next_left_position:
    :return:
    """

    box_1 = left_tangent.closest_point_on_line(
        right_position,
        contained=False
    )

    if box_1 is None:
        return [
            left_position,
            left_position,
            right_position,
            right_position
        ]

    box_2 = right_tangent.closest_point_on_line(
        left_position,
        contained=False
    )

    distance = box_1.distance_between(left_position)

    if last_left_position:
        prev_distance = box_1.distance_between(last_left_position)
    else:
        prev_distance = distance
        distance = box_1.distance_between(next_left_position)

    if distance < prev_distance:
        return [left_position, box_1, right_position, box_2]

    return [box_1, left_position, box_2, right_position]


def support_boxes(
        foot_positions: limb.Property,
        tangents: limb.Property
) -> dict:
    """

    :param foot_positions:
    :param tangents:
    :return:
    """

    fps = foot_positions
    rear_support_boxes = []
    rear_support_ranges = []
    forward_support_boxes = []
    forward_support_ranges = []

    count = len(tangents.left_pes)

    for i in range(count):
        before = fps.left_pes[i - 1] if i > 0 else None
        after = fps.left_pes[i + 1] if i < (count - 1) else None
        box = compute_support_box(
            left_position=foot_positions.left_pes[i],
            left_tangent=tangents.left_pes[i],
            right_position=foot_positions.right_pes[i],
            right_tangent=tangents.right_pes[i],
            last_left_position=before,
            next_left_position=after
        )
        rear_support_boxes.append(box)
        rear_support_ranges.append(box[0].distance_between(box[1]))

        before = fps.left_manus[i - 1] if i > 0 else None
        after = fps.left_manus[i + 1] if i < (count - 1) else None
        box = compute_support_box(
            left_position=foot_positions.left_manus[i],
            left_tangent=tangents.left_manus[i],
            right_position=foot_positions.right_manus[i],
            right_tangent=tangents.right_manus[i],
            last_left_position=before,
            next_left_position=after
        )
        forward_support_boxes.append(box)
        forward_support_ranges.append(box[0].distance_between(box[1]))

    return {
        'forward_boxes': forward_support_boxes,
        'rear_boxes': rear_support_boxes,
        'forward_ranges': forward_support_ranges,
        'rear_ranges': rear_support_ranges
    }



