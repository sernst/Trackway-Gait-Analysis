import os
import typing

import six

from tracksim import configs
from tracksim import generate
from tracksim import limb
from tracksim import trackway
from tracksim.trial import analyze, report, compute


def run(
        settings: typing.Union[str, dict],
        trackway_positions: trackway.TrackPosition = None,
        **kwargs) -> dict:
    """
    Runs and analyzes a simulation of the trackway under the conditions
    specified by the arguments and returns a dictionary of results for the trial

    :param settings:
        Either a dictionary containing the configuration values for the trial
        or an absolute path to a json format file that contains the
        configuration values for the trial
    :param trackway_positions:
        A TrackwayDefinition instance populated with phase and position values
    """

    settings = configs.load(settings, **kwargs)
    limb_phases = load_limb_phases(settings)
    trackway_positions = load_trackway_positions(settings, trackway_positions)

    trackway_definition = trackway.TrackwayDefinition(
        trackway_positions,
        limb_phases
    )
    trackway_definition.reorient_positions()

    foot_positions = limb.Property()

    time_steps = list(generate.time_steps_from_data(
        settings['steps_per_cycle'],
        trackway_definition
    ))

    for key in limb.KEYS:
        out = compute.positions_over_time(
            time_steps=time_steps,
            limb_positions=trackway_definition.limb_positions.get(key),
            limb_phase=trackway_definition.limb_phases.get(key),
            settings=settings
        )
        foot_positions.set(key, out)

    prune_invalid_positions(settings, time_steps, foot_positions)

    results = {
        'configs': settings,
        'times': time_steps,
        'positions': foot_positions,
        'couplings': analyze.coupling_distance(foot_positions),
        'separations': analyze.separations(foot_positions),
        'extensions': analyze.plane_limb_extensions(foot_positions)
    }

    if settings.get('report', True):
        results['report'] = report.create(
            settings, trackway_definition, results
        )

    return results


def load_limb_phases(settings: dict) -> limb.Property:
    """
    Returns the loaded limb phases as defined by the settings object

    :param settings:
        Configuration for the simulation trial
    """

    out = limb.Property()
    source = settings['limb_phases']

    if isinstance(source, (list, tuple)):
        return out.assign(*source)

    return out.assign(**source)


def load_trackway_positions(
        settings: dict,
        existing: limb.Property = None
) -> limb.Property:
    """
    Loads the trackway positions for the trial from the information provided in
    the settings object, unless an existing trackway positions object has been
    specified

    :param settings:
        Configuration for the simulation trial
    :param existing:
        Optionally the already loaded trackway positions, which will be cloned
        and returned if present
    """

    if existing:
        # Ignore if already specified
        return existing.clone()

    data = settings.get('data')

    if isinstance(data, six.string_types):
        # Load from a specified file
        if not data.startswith('/'):
            data = os.path.join(settings['path'], data)
        return trackway.load_positions_file(data)

    # Generate from configuration settings
    track_offsets = limb.Property().assign(*data['offsets'])
    return generate.trackway_positions(
        cycle_count=data['count'],
        step_size=data['step_size'],
        track_offsets=track_offsets,
        lateral_displacement=data['lateral_displacement']
    )


def prune_invalid_positions(
        settings: dict,
        time_steps: list,
        foot_positions: limb.Property
):
    """
    Iterates through the time_steps and foot_positions lists and removes values
    at the beginning and end where any invalid data is found. Such invalid data
    exists when some amount of time at the beginning or end of the simulation
    is valid for 1 or more of the limbs in the trackway, but not all 4.

    :param settings:
        Configuration for the simulation trial
    :param time_steps:
        A list of times at which the simulation calculated foot positions
    :param foot_positions:
        The calculated positions of each foot for each time step in the
        time_steps list
    """

    start_time = settings.get('start_time', 0)
    stop_time = settings.get('stop_time', 1e8)

    values = list(foot_positions.values())
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
