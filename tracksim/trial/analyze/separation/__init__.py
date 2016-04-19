
from tracksim import limb
from tracksim.reporting import Report

from tracksim.trial.analyze.separation import separation_calculate
from tracksim.trial.analyze.separation import separation_report


def calculate(foot_positions: limb.Property) -> dict:
    """

    :param foot_positions:
    :return:
    """

    lengths = separation_calculate.lengths(foot_positions)

    return dict(
        **lengths
    )


def add_to_report(report: Report, separation_data: dict, times: dict):
    """

    :param report:
    :param separation_data:
    :param times:
    :return:
    """

    separation_report.add_length_plot(report, separation_data, times)
