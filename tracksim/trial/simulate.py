import os
import typing

import six

from tracksim import configs
from tracksim import generate
from tracksim import limb
from tracksim import system
from tracksim import trackway
from tracksim.trial import analyze
from tracksim.trial import compute
from tracksim.trial import prune


def run(
        settings: typing.Union[str, dict],
        trackway_positions: trackway.TrackPosition = None,
        **kwargs
) -> dict:
    """
    Runs and analyzes a simulation of the trackway under the conditions
    specified by the arguments and returns a dictionary of results for the
    trial

    :param settings:
        Either a dictionary containing the configuration values for the trial
        or an absolute path to a json format file that contains the
        configuration values for the trial
    :param trackway_positions:
        A TrackwayDefinition instance populated with phase and position values
    """

    settings = configs.load('trial', settings, **kwargs)

    if 'steps_per_cycle' not in settings:
        settings['steps_per_cycle'] = 20
    if 'moving_ambiguity' not in settings:
        # The coefficient of uncertainty while the foot is moving
        settings['moving_ambiguity'] = 0.125
    if 'duty_cycle' not in settings:
        settings['duty_cycle'] = 0.6

    system.log('[{}]: STARTING'.format(settings['id']))

    activity_phases = load_activity_phases(settings)
    trackway_positions = load_trackway_positions(settings, trackway_positions)

    trackway_definition = trackway.TrackwayDefinition(
        trackway_positions,
        activity_phases
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
            activity_phase=trackway_definition.activity_phases.get(key),
            settings=settings
        )
        foot_positions.set(key, out)

    prune.invalid_positions(
        settings,
        time_steps,
        foot_positions
    )

    if len(time_steps) < 1:
        system.log(
            """
            [{}]: INVALID RESULTS
                There are no simulated results to analyze. Either the
                simulation is not valid, or you have set a start and end time
                that is not within the range of valid values. Please check your
                settings file.
            """.format(settings['id']))
        raise ValueError('Invalid Results')

    system.log('[{}]: ANALYZING'.format(settings['id']))

    reorientation_needed = prune.unused_foot_prints(
        trackway_definition.limb_positions,
        foot_positions
    )

    if reorientation_needed:
        # Reorient positions again now that the trackway has been pruned
        trackway_definition.reorient_positions(
            *foot_positions.left_pes,
            *foot_positions.right_pes,
            *foot_positions.left_manus,
            *foot_positions.right_manus
        )

    url = analyze.create(
        track_definition=trackway_definition,
        settings=settings,
        time_steps=time_steps,
        foot_positions=foot_positions
    )

    system.log('[{}]: COMPLETED'.format(settings['id']))

    return url


def load_activity_phases(settings: dict) -> limb.Property:
    """
    Returns the loaded activity phases as defined by the settings object

    :param settings:
        Configuration for the simulation trial
    """

    if 'activity_phases' in settings:
        settings['activity_phases'] = configs.to_phases_list(
            settings['activity_phases']
        )
    else:
        out = configs.support_to_activity_phases(
            settings['support_phases'],
            settings['duty_cycle']
        )

        # Zero the calculated settings around the lowest pes phase
        settings['activity_phases'] = [x - min(out[:2]) for x in out]

    if 'support_phases' in settings:
        settings['support_phases'] = configs.to_phases_list(
            settings['support_phases']
        )
    else:
        out = configs.activity_to_support_phases(
            settings['activity_phases'],
            settings['duty_cycle']
        )

        # Zero the calculated settings around the lowest pes phase
        settings['support_phases'] = [x - min(out[:2]) for x in out]

    out = limb.Property()
    source = settings['activity_phases']

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
        if not os.path.exists(data):
            system.log(
                """
                [ERROR]: No CSV source data exists at the path:

                    {}
                """.format(data)
            )
            raise FileNotFoundError('No CSV source file found')

        return trackway.load_positions_file(data)

    # Generate from configuration settings
    track_offsets = limb.Property().assign(*data['offsets'])
    return generate.trackway_positions(
        cycle_count=data['count'],
        step_size=data['step_size'],
        track_offsets=track_offsets,
        lateral_displacement=data['lateral_displacement'],
        positional_uncertainty=data.get('uncertainty')
    )

