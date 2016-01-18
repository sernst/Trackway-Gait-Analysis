
from tracksim import trackway

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
        A value between 0 and 1 that specified the relative phase of the limb
        compared to the reference limb within the trackway. A value of 0
        indicates that the limb is planted in the first position at t = 0,
        whereas a value of 1.0 indicates a limb is planted in the first
        position at time t = 1.0
    :param trial_configs:
        A dictionary of configuration values for the trial being simulated
    :return:
        The list of positions for the limb at the times specified by time_steps
        argument. The length of this locations list will be the same as the
        length of the time_steps argument.
    """

    out = []
    duty_cycle = trial_configs['duty_cycle']

    for time in time_steps:

        # Convert from world "lab" frame time to the time for this limb, which
        # removes its limb phase
        limb_frame_time = time - limb_phase
        count = len(limb_positions)

        if (count - 2) == time:
            out.append(limb_positions[-1].clone())
            continue

        if time >= (count - 2) or limb_frame_time < 0:
            # If the time is out of bounds append None
            out.append(None)
            continue

        try:
            out.append(position_at_limb_time(
                limb_time=limb_frame_time - int(limb_frame_time),
                before_position=limb_positions[int(limb_frame_time)],
                after_position=limb_positions[int(limb_frame_time) + 1],
                duty_cycle=duty_cycle,
                trial_configs=trial_configs))
        except Exception as err:
            raise

    return out

def position_at_limb_time(
        limb_time, before_position, after_position, duty_cycle, trial_configs):
    """
        During the duty cycle time period for the limb, the position will be
        located at the before position. After the duty cycle, the limb position
        is largely unknown because we have no evidence of the position, or even
        the accelerations and velocities, during that period. Therefore, the
        value returned if the midpoint between the before and after positions
        with a large uncertainty value that encompasses the region between
        the before and after positions.

    :param limb_time:
        A time on the range of [0,1] specific to that limb (no limb phase)
        where the limb will be at rest during the range [0, duty_cycle] and
        in motion to the next print during the range (duty_cycle, 1].
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

    if limb_time < duty_cycle:
        pos = before_position.clone()
        pos.annotation = 'FIXED'
        return pos

    bp = before_position
    ap = after_position
    progress = (limb_time - 0.5) / 0.5

    return trackway.TrackPosition.from_raw_values(
        x=bp.x.raw + progress*(ap.x.raw - bp.x.raw),
        x_uncertainty=max(
                ap.x.raw_uncertainty,
                abs(0.25*(ap.x.raw - bp.x.raw)) ),
        y=bp.y.raw + progress*(ap.y.raw - bp.y.raw),
        y_uncertainty=max(
                ap.y.raw_uncertainty,
                abs(0.25*(ap.y.raw - bp.y.raw)) ),
        annotation='MOVING')
