import os
import json
import typing
import glob

from tracksim import paths

def listings(
        report_type: str,
        results_path: str = None,
        matching_glob: str = None
) -> dict:
    """
    Returns a dictionary that contains the report ids and absolute paths to
    the corresponding data files.

    :param report_type:
    :param results_path:
    :param matching_glob:
    :return:
    """

    report_type = report_type.lower()[0]
    report_type = 'group' if report_type == 'g' else 'trial'

    if not results_path:
        results_path = paths.results()
    else:
        results_path = paths.clean(results_path)
    directory = os.path.join(results_path, 'reports', report_type)

    out = dict()

    if matching_glob:
        matching_glob = os.path.join(
            directory,
            matching_glob.strip(os.sep)
        )

        for item_path in glob.iglob(matching_glob):
            item_path = item_path.rstrip(os.sep)
            item = os.path.basename(item_path)
            out[item] = os.path.join(item_path, '{}.json'.format(item))

        return out

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item, '{}.json'.format(item))
        out[item] = item_path

    return out


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
        paths.clean(results_path),
        'reports',
        report_type,
        report_id,
        '{}.json'.format(report_id)
    )

    if not os.path.exists(path):
        return None

    with open(path, 'r+') as f:
        out = json.load(f)

    out['id'] = report_id
    return out


def all_by_type(
        report_type: str,
        results_path: str = None
) -> typing.List[dict]:
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


def group(
        group_id: str,
        results_path: str = None,
        load_trials: bool = True
) -> typing.Dict:
    """
    Loads the specified group and the trials associated with the group and
    returns them in a dictionary with the keys "group" for the group data and
    "trials" for each trial in group if load_trials is True.

    :param group_id:
        The unique identifier for the group to load
    :param results_path:
        The root directory where the simulation results are stored. If not
        specified, the default location will be used.
    :param load_trials:
        When True, the full results data for each trial will be included as
        well.
    :return:
    """

    group_data = read(
        report_type='group',
        report_id=group_id,
        results_path=results_path
    )

    if not load_trials:
        return dict(
            group=group_data,
            trials=[]
        )

    trials_data = []
    for trial_info in group_data['trials']:
        trial_data = read(
            report_type='trial',
            report_id=trial_info['id'],
            results_path=results_path
        )
        trial_data['group_id'] = group_id
        trial_data['group_index'] = len(trials_data)
        trials_data.append(trial_data)

    return dict(
        group=group_data,
        trials=trials_data
    )


def groups(
        matching_glob: str = None,
        results_path: str = None,
        load_trials: bool = True
) -> dict:
    """

    :param matching_glob:
    :param results_path:
    :param load_trials:
    :return:
    """

    group_matches = listings(
        report_type='group',
        results_path=results_path,
        matching_glob=matching_glob
    )

    groups_data = []
    trials_data = []
    for key in group_matches.keys():
        result = group(
            group_id=key,
            results_path=results_path,
            load_trials=load_trials
        )
        groups_data.append(result['group'])
        trials_data += result['trials']

    return dict(
        groups=groups_data,
        trials=trials_data
    )


def trial(trial_id: str, results_path: str = None) -> dict:
    """
    Returns the specified trial data

    :param trial_id:
        The unique identifier for the trial to load
    :param results_path:
        The root directory where the simulation results are stored. If not
        specified, the default location will be used.
    :return:
    """

    return read(
        report_type='trial',
        report_id=trial_id,
        results_path=results_path
    )


def trials(
        matching_glob: str = None,
        results_path: str = None
) -> list:
    """

    :param matching_glob:
    :param results_path:
    :return:
    """

    trials_matches = listings(
        report_type='trial',
        results_path=results_path,
        matching_glob=matching_glob
    )

    trials_data = []
    for key in trials_matches.keys():
        trials_data.append(
            trial(trial_id=key, results_path=results_path)
        )

    return trials_data
