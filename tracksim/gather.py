import os
import json
import typing

import tracksim


def results(report_type:str, path: str = None) -> typing.List[dict]:
    """
    Fetches the reported results for all simulations of the specified report
    type and returns them as a list of results dictionaries. Each result is
    modified with a 'gather' key that contains a dictionary with the absolute
    path and the filename of the source results file

    :param report_type:
        The type of report to gather. Valid types are 'groups' and 'trials'

    :param path:
        The report path where the results will be found. If no path is
        specified, the default report path will be used.
    """

    first_character = report_type[0].lower()
    if first_character == 't':
        report_type = 'trials'
    elif first_character == 'g':
        report_type = 'groups'

    if not path:
        path = tracksim.make_results_path(report_type)
    elif not path.endswith(report_type):
        path = os.path.join(path, report_type)

    if not os.path.exists(path):
        return []

    out = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if not os.path.isdir(item_path):
            continue

        json_path = os.path.join(path, item, '{}.json'.format(item))

        with open(json_path, 'r+') as f:
            data = json.load(f)
            data['gather'] = {'filename': item, 'path': item_path}
            out.append(data)

    return out


def group_results(path: str = None) -> dict:
    """

    :param path:
    :return:
    """

    groups = results('group', path)
    trials = []

    group_index = 0
    result_index = 0
    for g in groups:

        for trial_index in range(len(g['trials'])):
            trial = g['trials'][trial_index]

            trials.append({
                'index': result_index,
                'trial_index': trial_index,
                'group_index': group_index,
                'trial': trial,
                'group': g
            })

    return {
        'groups': groups,
        'trials': trials
    }
