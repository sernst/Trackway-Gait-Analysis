from tracksim import limb
from tracksim.reporting import Report
from tracksim.trial.analyze.coupling import coupling_calculate
from tracksim.trial.analyze.coupling import coupling_report


def calculate(foot_positions: limb.Property, times: dict) -> dict:
    """

    :param foot_positions:
    :param times:
    :return:
    """

    positions = coupling_calculate.positions(foot_positions, times)
    stats = coupling_calculate.statistics(positions)
    advances = coupling_calculate.advance(foot_positions, positions, times)

    return dict(
        **positions,
        **stats,
        **advances
    )


def add_to_report(report: Report, coupling_data: dict, times: dict):
    """

    :param report:
    :param coupling_data:
    :param times:
    :return:
    """

    coupling_report.plot_distribution(report, coupling_data)
    coupling_report.plot_lengths(report, coupling_data)
    coupling_report.plot_deviations(report, coupling_data)
    coupling_report.plot_advance(report, coupling_data)


def serialize(coupling_data: dict) -> dict:
    """

    :param coupling_data:
    :return:
    """

    out = dict(**coupling_data)

    keys = [
        'lengths', 'rear', 'forward', 'rear_advance', 'forward_advance',
        'midpoints', 'deviations'
    ]

    for k in keys:
        if k not in coupling_data:
            continue

        serialized = []
        for value in coupling_data[k]:
            serialized.append(value.serialize())
        out[k] = serialized

    out['value'] = coupling_data['value'].serialize()

    return out
