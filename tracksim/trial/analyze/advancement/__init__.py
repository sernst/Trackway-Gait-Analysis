from tracksim import limb
from tracksim.reporting import Report
from tracksim.trial.analyze.advancement import advancement_calculate
from tracksim.trial.analyze.advancement import advancement_report


def calculate(foot_positions: limb.Property, times: dict) -> dict:
    """

    :param foot_positions:
    :param times:
    :return:
    """

    limb_distances = advancement_calculate.strides(foot_positions, times)

    return dict(
        **limb_distances,
    )


def add_to_report(report: Report, advancement_data: dict, times: dict):
    """

    :param report:
    :param advancement_data:
    :param times:
    :return:
    """

    advancement_report.plot_strides(report, advancement_data)


def serialize(advancement_data: dict) -> dict:
    """

    :param advancement_data:
    :return:
    """

    out = dict(**advancement_data)

    keys = [
        'left_pes_strides',
        'right_pes_strides',
        'left_manus_strides',
        'right_manus_strides'
    ]

    for k in keys:
        if k not in advancement_data:
            continue

        serialized = []
        for value in advancement_data[k]:
            serialized.append(value.serialize())
        out[k] = serialized

    return out
