from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from tracksim import trackway

MOVING_ANNOTATION = 'M'
FIXED_ANNOTATION = 'F'

def positions_over_time(time_steps, limb_positions, limb_phase, trial_configs):
    """
        Creates a list containing the positions for the limb based on the
        specified arguments. Values that cannot be calculated because they are
        outside the temporal bounds given the data are set to None.

    :param time_steps:
        A iterable list of time steps over which to calculate the locations.
        The returned list will have a numeric or None value to match each value
        in this list.
    :param limb_positions:
        A list of TrackPosition instances for each position of the track within
        the trackway. These positions must be consecutive with no missing
        values, as the location computation assumes.
    :param limb_phase:
        A value of 0 indicates that the limb starts moving from the first track
        position to the second track position at time t = 0. A value of 0.5
        indicates that the limb starts moving from the first track position to
        the second track position at time t = 0.5.
    :param trial_configs:
        A dictionary of configuration values for the trial being simulated
    :return:
        The list of positions for the limb at the times specified by time_steps
        argument. The length of this locations list will be the same as the
        length of the time_steps argument.
    """

    out = []
    duty_cycle = trial_configs['duty_cycle']
    track_count = len(limb_positions)

    first_valid_time = limb_phase - duty_cycle
    last_valid_time = track_count - 1 + limb_phase

    for time in time_steps:

        # Convert from world "lab" frame time to the time for this limb, which
        # removes its limb phase
        limb_time = time - limb_phase
        limb_cycle = int(limb_time)

        if time < first_valid_time or time > last_valid_time:
            # If the time is out of bounds append None
            out.append(None)
            continue

        if limb_cycle < 0 or limb_time < 0:
            # While time is valid but the limb hasn't started its first valid
            # cycle, we can just use the first track position
            pos = limb_positions[0].clone()
            pos.annotation = FIXED_ANNOTATION
            out.append(pos)
            continue

        if (limb_cycle + 1) == track_count:
            # While time is still valid but the limb has finished all of its
            # active cycles, we just use the last track position
            pos = limb_positions[-1].clone()
            pos.annotation = FIXED_ANNOTATION
            out.append(pos)
            continue

        try:
            out.append(position_at_cycle_time(
                cycle_time=limb_time - limb_cycle,
                before_position=limb_positions[limb_cycle],
                after_position=limb_positions[limb_cycle + 1],
                duty_cycle=duty_cycle,
                trial_configs=trial_configs))
        except Exception as err:
            raise

    return out

def position_at_cycle_time(
        cycle_time, before_position, after_position, duty_cycle, trial_configs):
    """
        During the duty cycle time period for the limb, the position will be
        located at the before position. After the duty cycle, the limb position
        is largely unknown because we have no evidence of the position, or even
        the accelerations and velocities, during that period. Therefore, the
        value returned if the midpoint between the before and after positions
        with a large uncertainty value that encompasses the region between
        the before and after positions.

    :param cycle_time:
        A time on the range of [0,1] specific to that limb (no limb phase)
        where the limb will be moving during the range [0, 1.0 - duty_cycle]
        and at rest on the next position during the range (1.0 - duty_cycle, 1).
    :param before_position:
        The position of the limb at the start of the limb time
    :param after_position:
        The position of the limb at the end of the limb time
    :param duty_cycle:
        The duty cycle for the limb
    :param trial_configs:
        The dictionary of configuration settings for the specified trial
    :return:
        A TrackPosition instance representing the position of a track at the
        given time.
    """

    move_time = (1.0 - duty_cycle)

    if cycle_time >= move_time:
        pos = after_position.clone()
        pos.annotation = FIXED_ANNOTATION
        return pos

    bp = before_position
    ap = after_position
    progress = max(0.0, min(1.0, cycle_time / move_time))

    return trackway.TrackPosition.from_raw_values(
        x=bp.x.raw + progress*(ap.x.raw - bp.x.raw),
        x_uncertainty=max(
                ap.x.raw_uncertainty,
                abs(0.25*(ap.x.raw - bp.x.raw)) ),
        y=bp.y.raw + progress*(ap.y.raw - bp.y.raw),
        y_uncertainty=max(
                ap.y.raw_uncertainty,
                abs(0.25*(ap.y.raw - bp.y.raw)) ),
        annotation=MOVING_ANNOTATION)
