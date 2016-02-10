
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import six

import tracksim
from tracksim import analysis
from tracksim import compute
from tracksim import generate
from tracksim import report
from tracksim import trackway

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

    trial_configs = load_trial_configs(trial_configs, **kwargs)

    limb_phases = tracksim.LimbProperty().assign(*trial_configs['limb_phases'])

    trackway_positions = load_trackway_positions(
        trackway_positions,
        trial_configs
    )

    trackway_definition = trackway.TrackwayDefinition(
        limb_positions=trackway_positions,
        limb_phases=limb_phases)
    trackway_definition.reorient_positions()

    foot_positions = tracksim.LimbProperty()

    time_steps = generate.time_steps_from_data(
        steps_per_cycle=trial_configs['steps_per_cycle'],
        trackway_definition=trackway_definition)

    for key in tracksim.LimbProperty.LIMB_KEYS:
        foot_positions.set(key, compute.positions_over_time(
            time_steps=time_steps,
            limb_positions=trackway_definition.limb_positions.get(key),
            limb_phase=trackway_definition.limb_phases.get(key),
            trial_configs=trial_configs
        ))

    time_steps = list(time_steps)
    prune_invalid_positions(time_steps, foot_positions)

    results = {
        'times': time_steps,
        'positions': foot_positions,
        'gals': analysis.calculate_gal(foot_positions),
        'extensions': analysis.calculate_extensions(foot_positions)
    }

    if trial_configs.get('report', True):
        report.create(trial_configs, trackway_definition, results)

    return results

def load_trial_configs(source, **kwargs):
    """

    :param source:
    :return:
    """

    if isinstance(source, str):
        path = source
        with open(path, 'r+') as f:
            source = json.load(f)
        source['path'] = os.path.dirname(path)

    for k, v in kwargs.items():
        source[k] = v

    return source

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
    track_offsets = tracksim.LimbProperty().assign(*data['offsets'])
    return generate.trackway_positions(
        count=data['count'],
        step_size=data['step_size'],
        track_offsets=track_offsets,
        lateral_displacement=data['lateral_displacement']
    )

def prune_invalid_positions(time_steps, results):
    """

    :param time_steps:
    :param results:
    :return:
    """

    values = results.values()
    values.append(time_steps)
    index = 0

    while index < len(values[0]):
        entries = []
        for v in values:
            entries.append(v[index])

        if None in entries or entries[-1] < 0:
            for v in values:
                v[index:index+1] = []
        else:
            index += 1
