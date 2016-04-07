from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import six

from tracksim import configs
from tracksim import generate
from tracksim import limb
from tracksim import trackway
from tracksim.trial import analyze, report, compute


def run(trial_configs, trackway_positions = None, **kwargs):
    """
        Runs and analyzes a simulation of the trackway under the conditions
        specified by the arguments

    :param trial_configs:
        Either a dictionary containing the configuration values for the trial
        or an absolute path to a json format file that contains the
        configuration values for the trial
    :param trackway_positions:
        A TrackwayDefinition instance populated with phase and position values
    :return:
    """

    trial_configs = configs.load(trial_configs, **kwargs)

    limb_phases = limb.Property().assign(*trial_configs['limb_phases'])

    trackway_positions = load_trackway_positions(
        trackway_positions,
        trial_configs
    )

    trackway_definition = trackway.TrackwayDefinition(
        limb_positions=trackway_positions,
        limb_phases=limb_phases)
    trackway_definition.reorient_positions()

    foot_positions = limb.Property()

    time_steps = generate.time_steps_from_data(
        steps_per_cycle=trial_configs['steps_per_cycle'],
        trackway_definition=trackway_definition)

    for key in limb.KEYS:
        foot_positions.set(key, compute.positions_over_time(
            time_steps=time_steps,
            limb_positions=trackway_definition.limb_positions.get(key),
            limb_phase=trackway_definition.limb_phases.get(key),
            trial_configs=trial_configs
        ))

    time_steps = list(time_steps)
    prune_invalid_positions(trial_configs, time_steps, foot_positions)

    results = {
        'configs': trial_configs,
        'times': time_steps,
        'positions': foot_positions,
        'couplings': analyze.coupling_distance(foot_positions),
        'separations': analyze.separations(foot_positions),
        'extensions': analyze.plane_limb_extensions(
            foot_positions
        )
    }

    if trial_configs.get('report', True):
        results['report'] = report.create(
            trial_configs, trackway_definition, results
        )

    return results

def load_trackway_positions(source, trial_configs, **kwargs):
    """

    :param source:
    :param trial_configs:
    :param kwargs:
    :return:
    """

    if source:
        # Ignore if already specified
        return source

    data = trial_configs.get('data')

    if isinstance(data, six.string_types):
        # Load from a specified file
        if not data.startswith('/'):
            data = os.path.join(trial_configs['path'], data)
        return trackway.load_positions_file(data)

    # Generate from configuration settings
    track_offsets = limb.Property().assign(*data['offsets'])
    return generate.trackway_positions(
        count=data['count'],
        step_size=data['step_size'],
        track_offsets=track_offsets,
        lateral_displacement=data['lateral_displacement']
    )


def prune_invalid_positions(trial_configs, time_steps, results):
    """

    :param configs:
    :param time_steps:
    :param results:
    :return:
    """

    start_time = trial_configs.get('start_time', 0)
    stop_time = trial_configs.get('stop_time', 1e8)

    values = list(results.values())
    values.append(time_steps)
    index = 0

    while index < len(values[0]):
        entries = []
        for v in values:
            entries.append(v[index])

        cull = (
            None in entries or
            entries[-1] < start_time or
            entries[-1] > stop_time
        )

        if cull:
            for v in values:
                v[index:index+1] = []
        else:
            index += 1
