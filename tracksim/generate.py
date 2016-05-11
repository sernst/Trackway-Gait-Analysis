import typing

import numpy as np

import measurement_stats as mstats
from tracksim import limb
from tracksim import trackway


def time_steps_from_data(
        steps_per_cycle: int,
        trackway_definition: trackway.TrackwayDefinition
) -> np.ndarray:
    """
    Creates an array of time steps based on the number of steps per cycle and
    the information stored in the trackway_definition. This works like the
    time_steps method, but the minimum and maximum times are determined
    automatically based on the trackway_definition.

    :param steps_per_cycle:
        The number of time steps in each cycle, where a cycle is defined as a
        unit amount of time (1.0, 2.0, 3.0, ...).
    :param trackway_definition:
        The positional information for the trackway
    """

    max_time = 0
    for key in limb.KEYS:
        track_count = trackway_definition.limb_positions.get(key)
        max_time = max(max_time, len(track_count))

    return time_steps(steps_per_cycle, -1.0, max_time)


def time_steps(
        steps_per_cycle: int,
        min_time: float,
        max_time: float
) -> np.ndarray:
    """
    Creates an evenly spaced Numpy array of time steps between the min and max
    times inclusively where the spacing is determined by the steps_per_cycle.

    :param steps_per_cycle:
        The number of time steps in each cycle, where a cycle is defined as a
        unit amount of time (1.0, 2.0, 3.0, ...).
    :param min_time:
        The time at which to start the time step array
    :param max_time:
        The time at which to end the time step array
    """

    return np.linspace(
        start=min_time,
        stop=max_time,
        num=steps_per_cycle * (max_time - min_time) + 1
    )


def trackway_data(
        cycle_count: int,
        step_size: float,
        activity_phases: limb.Property,
        track_offsets: limb.Property,
        lateral_displacement: typing.Union[float, list, tuple],
        positional_uncertainty: float = None
) -> trackway.TrackwayDefinition:
    """
    Creates a simulated trackway definition with trackway positions calculated
    based on the arguments

    :param cycle_count:
        The number cycles to include in the simulation data
    :param step_size:
        The length (in meters) between successive steps for each limb in the
        trackway
    :param activity_phases:
        The phases for each limb, which is the standard phases object used by
        both
    :param track_offsets:
        The spatial offsets for each limb in the trackway.
    :param lateral_displacement:
        The lateral distance from the mid-line for each limb
    :param positional_uncertainty:
        The amount of uncertainty in the x and y positions for each track
        in the trackway
    """

    return trackway.TrackwayDefinition(
        activity_phases=activity_phases,
        limb_positions=trackway_positions(
            cycle_count=cycle_count,
            step_size=step_size,
            track_offsets=track_offsets,
            lateral_displacement=lateral_displacement,
            positional_uncertainty=positional_uncertainty
        ))


def trackway_positions(
        cycle_count: int,
        step_size: float,
        track_offsets: limb.Property,
        lateral_displacement: typing.Union[float, list, tuple],
        positional_uncertainty: float = None,
) -> limb.Property:
    """
    Creates a limb Property with trackway positions for each limb based on the
    specified arguments

    :param cycle_count:
        The number cycles to include in the simulation data
    :param step_size:
        The length (in meters) between successive steps for each limb in the
        trackway
    :param track_offsets:
        The spatial offsets for each limb in the trackway.
    :param lateral_displacement:
        The lateral distance from the mid-line for each limb
    :param positional_uncertainty:
        The amount of uncertainty in the x and y positions for each track
        in the trackway
    """

    assert isinstance(track_offsets, limb.Property), \
        'Phases must be a limb property'

    if isinstance(lateral_displacement, (list, tuple)):
        pes_lateral_displacement = lateral_displacement[0]
        manus_lateral_displacement = lateral_displacement[1]
    else:
        pes_lateral_displacement = lateral_displacement
        manus_lateral_displacement = lateral_displacement

    return limb.Property(
        left_pes=track_positions(
            cycle_count=cycle_count,
            step_size=step_size,
            track_offset=track_offsets.left_pes,
            lateral_displacement=pes_lateral_displacement,
            positional_uncertainty=positional_uncertainty
        ),
        right_pes=track_positions(
            cycle_count=cycle_count,
            step_size=step_size,
            track_offset=track_offsets.right_pes,
            lateral_displacement=-pes_lateral_displacement,
            positional_uncertainty=positional_uncertainty
        ),
        left_manus=track_positions(
            cycle_count=cycle_count,
            step_size=step_size,
            track_offset=track_offsets.left_manus,
            lateral_displacement=manus_lateral_displacement,
            positional_uncertainty=positional_uncertainty
        ),
        right_manus=track_positions(
            cycle_count=cycle_count,
            step_size=step_size,
            track_offset=track_offsets.right_manus,
            lateral_displacement=-manus_lateral_displacement,
            positional_uncertainty=positional_uncertainty
        )
    )


def track_positions(
        cycle_count: int,
        step_size: float,
        track_offset: float,
        lateral_displacement: float,
        positional_uncertainty: float = None
) -> list:
    """
    Creates a list of trackway positions for a limb based on the
    specified arguments

    :param cycle_count:
        The number cycles to include in the simulation data
    :param step_size:
        The length (in meters) between successive steps for each limb in the
        trackway
    :param track_offset:
        The spatial offsets for each limb in the trackway.
    :param lateral_displacement:
        The lateral distance from the mid-line for each limb
    :param positional_uncertainty:
        The amount of uncertainty in the x and y positions for each track
        in the trackway
    """

    out = []

    if positional_uncertainty is None:
        positional_uncertainty = 0.01

    for i in range(cycle_count):
        out.append(trackway.TrackPosition(
            x=mstats.value.ValueUncertainty(
                value=(track_offset + i) * step_size,
                uncertainty=positional_uncertainty
            ),
            y=mstats.value.ValueUncertainty(
                value=lateral_displacement,
                uncertainty=positional_uncertainty
            )
        ))

    return out






