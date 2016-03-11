from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from datetime import datetime

from tracksim import configs
from tracksim.group import analyze
from tracksim.group import report
from tracksim.trial import simulate as simulate_trial

def run(group_configs, **kwargs):
    """

    :param group_configs:
    :param kwargs:
    :return:
    """

    group_configs = configs.load(group_configs, **kwargs)
    start_time = datetime.utcnow()
    trials = []

    for filename in group_configs.get('trials', []):
        path = os.path.abspath(os.path.join(group_configs['path'], filename))

        trials_configs = configs.load(path, group=group_configs)
        trial_results = simulate_trial.run(trials_configs)

        trials.append(dict(
            configs=trials_configs,
            results=trial_results,
            index=len(trials) + 1,
            id=trials_configs['name'].replace(' ', '-'),
        ))

    results = dict(
        couplings=analyze.coupling_distribution_data(trials)
    )

    results['report'] = report.write(start_time, group_configs, results, trials)

    return results
