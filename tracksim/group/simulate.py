import os
import typing

import tracksim
from tracksim import configs
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

    tracksim.log('[{}]: STARTING'.format(settings['id']))

    for source in settings.get('trials', []):
        if isinstance(source, str):
            original = source
            source = os.path.abspath(os.path.join(settings['path'], source))
            if not os.path.exists(source):
                source = '{}.json'.format(source)
            if not os.path.exists(source):
                tracksim.log(
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

    tracksim.log('[{}]: ANALYZING'.format(settings['id']))

    url = analyze.create(settings, trials)

    tracksim.log('[{}]: COMPLETE'.format(settings['id']))

    return url
