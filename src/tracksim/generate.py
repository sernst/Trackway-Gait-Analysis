
import numpy as np

import tracksim
from tracksim import number
from tracksim import trackway

def time_steps_from_data(steps_per_cycle, trackway_definition):
    """

    :param steps_per_cycle:
    :param trackway_definition:
    :return:
    """

    max_time = 0
    for key in tracksim.LimbProperty.LIMB_KEYS:
        track_count = trackway_definition.limb_positions.get(key)
        max_time = max(max_time, len(track_count))

    return time_steps(steps_per_cycle, -1.0, max_time)

def time_steps(steps_per_cycle, min_time, max_time):
    """

    :param steps_per_cycle:
    :param min_time:
    :param max_time:
    :return:
    """

    return np.linspace(
            start=min_time,
            stop=max_time,
            num=steps_per_cycle * (max_time - min_time) + 1)

def trackway_data(
        count, step_size, limb_phases, limb_offsets, lateral_displacement):
    """

    :param count:
    :param step_size:
    :param limb_phases:
    :param limb_offsets:
    :param lateral_displacement:
    :return:
    """

    return trackway.TrackwayDefinition(
        limb_phases=limb_phases,
        limb_positions=trackway_positions(
            count=count,
            step_size=step_size,
            track_offsets=limb_offsets,
            lateral_displacement=lateral_displacement ))

def trackway_positions(count, step_size, track_offsets, lateral_displacement):
    """

    :param count:
    :param step_size:
    :param track_offsets:
    :param lateral_displacement:
    :return:
    """

    assert isinstance(track_offsets, tracksim.LimbProperty), \
        'Phases must be a limb property'

    if isinstance(lateral_displacement, (list, tuple)):
        pes_lateral_displacement = lateral_displacement[0]
        manus_lateral_displacement = lateral_displacement[1]
    else:
        pes_lateral_displacement = lateral_displacement
        manus_lateral_displacement = lateral_displacement

    return tracksim.LimbProperty(
        left_pes=track_positions(
            count=count,
            step_size=step_size,
            limb_offset=track_offsets.left_pes,
            lateral_displacement=pes_lateral_displacement),
        right_pes=track_positions(
            count=count,
            step_size=step_size,
            limb_offset=track_offsets.right_pes,
            lateral_displacement=-pes_lateral_displacement),
        left_manus=track_positions(
            count=count,
            step_size=step_size,
            limb_offset=track_offsets.left_manus,
            lateral_displacement=manus_lateral_displacement),
        right_manus=track_positions(
            count=count,
            step_size=step_size,
            limb_offset=track_offsets.right_manus,
            lateral_displacement=-manus_lateral_displacement) )

def track_positions(count, step_size, limb_offset, lateral_displacement):
    """

    :param count:
    :param step_size:
    :param limb_offset:
    :param lateral_displacement:
    :return:
    """

    out = []

    for i in range(count):
        out.append(trackway.TrackPosition(
            x=number.ValueUncertainty(
                value=(limb_offset + i) * step_size,
                uncertainty=0.01),
            y=number.ValueUncertainty(
                value=lateral_displacement,
                uncertainty=0.01) ))

    return out






