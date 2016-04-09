import os
import typing
from datetime import datetime

import tracksim
from tracksim import configs
from tracksim.group import analyze
from tracksim.group import report
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

    settings = configs.load(settings, **kwargs)
    start_time = datetime.utcnow()
    trials = []

    tracksim.log('[{}]: STARTING'.format(settings['id']))

    for source in settings.get('trials', []):
        if isinstance(source, str):
            source = os.path.abspath(
                os.path.join(settings['path'], source)
            )

        trial_settings = configs.load(source, inherits=settings)
        trial_results = simulate_trial.run(trial_settings)
        trials.append(dict(
            configs=trial_settings,
            results=trial_results,
            index=len(trials) + 1,
            id=trial_settings['id'],
        ))

    tracksim.log('[{}]: ANALYZING'.format(settings['id']))

    results = dict(
        couplings=analyze.coupling_distribution_data(trials),
        trials=trials
    )

    results['report'] = report.create(start_time, settings, results, trials)

    tracksim.log('[{}]: COMPLETE'.format(settings['id']))

    return results
