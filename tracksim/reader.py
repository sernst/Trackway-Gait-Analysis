import os
import json
import typing

from tracksim import paths


def read(report_type: str, report_id: str, results_path: str = None) -> dict:
    """

    :param report_type:
    :param report_id:
    :param results_path:
    :return:
    """

    first_character = report_type[0].lower()
    if first_character == 't':
        report_type = 'trial'
    elif first_character == 'g':
        report_type = 'group'

    if not results_path:
        results_path = paths.results()
    path = os.path.join(
        results_path, 'reports', report_type,
        report_id, '{}.json'.format(report_id)
    )

    if not os.path.exists(path):
        return None

    with open(path, 'r+') as f:
        out = json.load(f)

    out['id'] = report_id
    return out


def all_by_type(report_type: str, results_path: str = None) -> typing.List[dict]:
    """
    Fetches the reported results for all simulations of the specified report
    type and returns them as a list of results dictionaries.

    :param report_type:
        The type of report to gather. Valid types are 'groups' and 'trials'

    :param results_path:
        The report path where the results will be found. If no path is
        specified, the default report path will be used.
    """

    first_character = report_type[0].lower()
    if first_character == 't':
        report_type = 'trial'
    elif first_character == 'g':
        report_type = 'group'

    if not results_path:
        results_path = paths.results()

    path = os.path.join(results_path, 'reports', report_type)

    if not os.path.exists(path):
        return []

    out = []

    for report_id in os.listdir(path):
        data = read(report_type, report_id, results_path=results_path)
        if data:
            out.append(data)

    return out


def all_groups(results_path: str = None) -> dict:
    """

    :param results_path:
    :return:
    """

    groups = all_by_type('group', results_path)
    trials = []

    group_index = 0
    global_index = 0
    for g in groups:
        g['index'] = group_index

        for t in g['trials']:
            t['group'] = g
            t['global_index'] = global_index
            trials.append(t)

            global_index += 1
        group_index += 1

    return {
        'groups': groups,
        'trials': trials
    }
