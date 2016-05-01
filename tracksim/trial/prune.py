from tracksim import limb


def invalid_positions(
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

    was_culled = False

    start_time = settings.get('start_time', 0)
    end_time = settings.get('end_time', 1e8)

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
            entries[-1] > end_time
        )

        if cull:
            was_culled = True
            for v in values:
                v[index:index + 1] = []
        else:
            index += 1

    return was_culled


def unused_foot_prints(
        print_positions: limb.Property,
        foot_positions: limb.Property
):
    """
    Trims the print positions lists to include only those positions found in
    the foot positions lists and the positions just before and after to provide
    context

    :param print_positions:
    :param foot_positions:
    :return:
    """

    was_pruned = False

    def is_in(uid: str, items: list) -> bool:
        for item in items:
            if item.uid == uid:
                return True
        return False

    for limb_key, foot_prints in print_positions.items():

        index = len(foot_prints) - 1
        while index > 0:
            index -= 1
            if is_in(foot_prints[index].uid, foot_positions.get(limb_key)):
                break
            foot_prints.pop()
            was_pruned = True

        while len(foot_prints) > 1:
            if is_in(foot_prints[1].uid, foot_positions.get(limb_key)):
                break
            foot_prints.pop(0)
            was_pruned = True

    return was_pruned
