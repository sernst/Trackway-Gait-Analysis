from tracksim import limb
from tracksim.reporting import Report
from tracksim.trial.analyze.tangent import tangent_calculate


def calculate(foot_positions: limb.Property) -> dict:
    """

    :param foot_positions:
    :return:
    """

    tangents = tangent_calculate.create_tangents(foot_positions)
    support_boxes = tangent_calculate.support_boxes(foot_positions, tangents)

    return dict(
        tangents=tangents,
        **support_boxes
    )


def add_to_report(report: Report, tangent_data: dict, times: dict):
    """

    :param report:
    :param tangent_data:
    :param times:
    :return:
    """

    pass


def serialize(tangent_data: dict) -> dict:
    """

    :param tangent_data:
    :return:
    """

    out = dict(**tangent_data)

    tangents = dict()
    for k in limb.KEYS:
        serialized = []
        for tan in tangent_data['tangents'].get(k):
            serialized.append(tan.serialize())
        tangents[k] = serialized
    out['tangents'] = tangents

    forward_boxes = []
    for box in tangent_data['forward_boxes']:
        forward_boxes.append([x.serialize() for x in box])
    out['forward_boxes'] = forward_boxes

    rear_boxes = []
    for box in tangent_data['rear_boxes']:
        rear_boxes.append([x.serialize() for x in box])
    out['rear_boxes'] = rear_boxes

    keys = ['forward_ranges', 'rear_ranges']
    for k in keys:
        if k not in tangent_data:
            continue

        serialized = []
        for value in tangent_data[k]:
            serialized.append(value.serialize())
        out[k] = serialized

    return out

