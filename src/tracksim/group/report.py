from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json

import measurement_stats as mstats

import tracksim

def write(start_time, group_configs, analysis, trials):
    """

    :param start_time:
    :param configs:
    :param analysis:
    :param trials:
    :return:
    """

    group_id = group_configs['name'].replace(' ', '-')
    filename = '{}.json'.format(group_id)

    out = dict(
        id=group_id,
        configs=group_configs,
        trials=make_trial_data(trials),
        couplings=make_coupling_data(analysis['couplings'], trials)
    )

    output_directory = tracksim.make_results_path('report', 'groups', group_id)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    path = os.path.join(output_directory, filename)
    with open(path, 'w+') as f:
        json.dump(out, f)

    return out

def make_trial_data(trials):
    """

    :param trials:
    :return:
    """

    out = []

    for t in trials:
        out.append(dict(
            index=t['index'],
            id=t['id'],
            name=t['configs']['name'],
            summary=t['configs'].get('summary', '')
        ))

    return out

def make_coupling_data(source, trials):
    """

    :param source:
    :param trials:
    :return:
    """

    dists = []
    bounds = []

    min_value = 1e6
    max_value = -1e6
    for t in trials:
        couplings = t['results']['couplings']

        bounds.append(couplings['bounds'])

        dist = mstats.density.create_distribution(couplings['data'])
        min_value = min(min_value, dist.minimum_boundary(3))
        max_value = max(max_value, dist.maximum_boundary(3))
        dists.append(dist)

    x_values = mstats.ops.linear_space(min_value, max_value, 250)

    densities = []
    populations = []
    for dist in dists:
        populations.append(mstats.density.ops.population(dist, 256))
        densities.append(dist.probabilities_at(x_values))

    vals, uncs = mstats.values.unzip(source['values'])

    return dict(
        values=vals,
        uncertainties=uncs,
        populations=populations,
        bounds=bounds,
        densities={
            'x':x_values,
            'series':densities
        }
    )
