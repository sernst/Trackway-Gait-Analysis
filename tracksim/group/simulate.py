import os
import typing
from datetime import datetime

from tracksim import configs
from tracksim.group import analyze
from tracksim.group import report
from tracksim.trial import simulate as simulate_trial

def run(
        group_configs: typing.Union[str, dict],
        on_trial_start: typing.Callable[[dict], None] = None,
        on_trial_complete: typing.Callable[[dict, dict], None] = None,
        **kwargs
) -> dict:
    """
    Executes a grouped collection of simulation trials and returns the compiled
    results for the individual trials, as well as results calculated for the
    group of trials

    :param group_configs:
        Settings for running the group of trials. Each trial configuration
        will inherit values from these settings.
    :param on_trial_start:
        A callback executed before each trial starts running, with the
        loaded configuration settings object for that trial as the argument
    :param on_trial_complete:
        A callback executed after each trial completes, with the simulation
        results for that trial as the argument

    :param kwargs:
        Optional setting overrides to be included in the group configuration
    """

    group_configs = configs.load(group_configs, **kwargs)
    start_time = datetime.utcnow()
    trials = []

    for source in group_configs.get('trials', []):
        if isinstance(source, str):
            source = os.path.abspath(
                os.path.join(group_configs['path'], source)
            )

        trials_configs = configs.load(source, inherits=group_configs)

        if on_trial_start is not None:
            on_trial_start(trials_configs)

        trial_results = simulate_trial.run(trials_configs)

        trials.append(dict(
            configs=trials_configs,
            results=trial_results,
            index=len(trials) + 1,
            id=trials_configs['name'].replace(' ', '-'),
        ))

        if on_trial_complete is not None:
            on_trial_complete(trials_configs, trial_results)

    results = dict(
        couplings=analyze.coupling_distribution_data(trials)
    )

    results['report'] = report.create(start_time, group_configs, results, trials)

    return results
