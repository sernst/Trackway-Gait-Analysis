import os
import typing
from datetime import datetime

import measurement_stats as mstats

from tracksim import reporting


def create(
        start_time: datetime,
        group_configs: dict,
        analysis: dict,
        trials: typing.List[dict]
) -> dict:
    """
    Creates a group report dictionary and writes it to the group report
    directory as well as returning it

    :param start_time:
        The datetime when the group of simulations started
    :param group_configs:
        Configuration for the group
    :param analysis:
        Group analysis dictionary
    :param trials:
        List of trial simulation results
    """

    group_id = group_configs['name'].replace(' ', '-')

    root_report_path = reporting.initialize_output_directory(
        group_configs.get('report_path')
    )

    out = dict(
        root_path=root_report_path,
        run_time=start_time.isoformat(),
        id=group_id,
        configs=group_configs,
        trials=make_trial_data(trials),
        couplings=make_coupling_data(analysis['couplings'], trials)
    )

    output_directory = os.path.join(root_report_path, 'groups', group_id)
    reporting.write_javascript_files(
        directory=output_directory,
        sim_id=group_id,
        key='SIM_DATA',
        data=out
    )

    return out


def make_trial_data(trial_results: typing.List[dict]) -> list:
    """
    Returns a list of trial pruned data information from the trial simulation
    results list that is relevant for group reporting

    :param trial_results:
        Simulation results for each trial run by the group
    """

    out = []

    for t in trial_results:
        out.append(dict(
            index=t['index'],
            id=t['id'],
            name=t['configs']['name'],
            summary=t['configs'].get('summary', '')
        ))

    return out


def make_coupling_data(coupling_data, trial_results):
    """
    Generates coupling report data from the analyzed coupling data and the
    individual simulation trial results

    :param coupling_data:
        Grouped coupling data from the grouped simulation results
    :param trial_results:
        Simulation results for each trial run by the group
    """

    dists = []
    bounds = []

    min_value = 1e6
    max_value = -1e6
    for t in trial_results:
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

    values, uncertainties = mstats.values.unzip(coupling_data['values'])

    return dict(
        values=values,
        uncertainties=uncertainties,
        populations=populations,
        bounds=bounds,
        densities={
            'x':x_values,
            'series':densities
        }
    )
