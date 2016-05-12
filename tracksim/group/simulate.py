import os
import json
import typing

from tracksim import configs
from tracksim import paths
from tracksim import system
from tracksim.group import analyze
from tracksim.trial import simulate as simulate_trial


def run(
        settings: typing.Union[str, dict],
        **kwargs
) -> dict:
    """
    Executes a grouped collection of simulation trials and returns the compiled
    results for the individual trials, as well as results calculated for the
    group of trials

    :param settings:
        Settings for running the group of trials. Each trial configuration
        will inherit values from these settings.
    :param kwargs:
        Optional setting overrides to be included in the group configuration
    """

    settings = configs.load('group', settings, **kwargs)
    trials = []

    system.log('[{}]: STARTING'.format(settings['id']))

    for source in fetch_trial_list(settings):
        if isinstance(source, str):
            original = source
            source = os.path.abspath(os.path.join(settings['path'], source))
            if not os.path.exists(source):
                source = '{}.json'.format(source)
            if not os.path.exists(source):
                system.log(
                    """
                    [ERROR]: Unable to locate simulation trial file "{}"
                    """.format(original)
                )
                raise FileNotFoundError('No such file {}'.format(source))

        trial_settings = configs.load('trial', source, inherits=settings)
        simulate_trial.run(trial_settings)
        trials.append(dict(
            settings=trial_settings,
            index=len(trials) + 1,
            id=trial_settings['id'],
        ))

    system.log('[{}]: ANALYZING'.format(settings['id']))

    url = analyze.create(settings, trials)

    system.log('[{}]: COMPLETE'.format(settings['id']))

    return url


def fetch_trial_list(settings: dict) -> list:
    """

    :param settings:
    :return:
    """

    trials = settings.get('trials', [])

    if isinstance(trials, (list, tuple)):
        return trials

    if not isinstance(trials, str):
        trials = ''

    if not trials:
        directory = settings['path']
    else:
        directory = paths.clean(os.path.join(settings['path'], trials))

    if not os.path.exists(directory):
        return []

    out = []
    for item in os.listdir(directory):
        if not item.endswith('.json'):
            continue

        item_path = os.path.join(directory, item)
        try:
            with open(item_path, 'r+') as f:
                contents = json.load(f)
        except Exception:
            continue

        if 'trials' in contents:
            continue

        if 'name' in contents:
            out.append(item)
    return out
