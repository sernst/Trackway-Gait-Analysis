from tracksim import reader
from tracksim.coupling.plotting import styles
import pandas as pd
import typing
import numpy as np


def to_data_entry(trial: dict) -> dict:
    """

    :param trial:
    :return:
    """

    gait_id, remainder = trial['id'].split('-', 1)
    gait_name = remainder.split('_', 1)[0]

    try:
        separation = int(gait_name[-1])
        gait_name = gait_name[:-1]
    except Exception:
        separation = 1

    duty_cycle = int(100 * trial['settings']['duty_cycle'])
    short_id = '{}-{} ({}%)'.format(gait_id, separation, duty_cycle)

    return dict(
        id=trial['id'],
        short_id=short_id,
        duty_cycle=duty_cycle,
        gait_id=gait_id,
        gait_index=int(gait_id[1]),
        gait_name=gait_name,
        separation=separation,
        coupling_length=trial['couplings']['value']['value'],
        uncertainty=trial['couplings']['value']['uncertainty'],
        start_time=trial['times']['cycles'][0],
        end_time=trial['times']['cycles'][-1],
        color=styles.GAIT_COLORS[int(gait_id[1])]
    )


def load(
        group_ids: list = None,
        trial_ids: list = None,
        row_filter: typing.Callable = None
):
    """

    :param group_ids:
    :param trial_ids:
    :param row_filter:
    :return:
    """

    if not group_ids:
        group_ids = []
    groups = [reader.group(gid) for gid in group_ids]

    if not trial_ids:
        trial_ids = []
    trials = [reader.trial(tid) for tid in trial_ids]

    for g in groups:
        trials += g['trials']

    df = []
    for trial in trials:
        df.append(to_data_entry(trial))
        trial['short_id'] = df[-1]['short_id']

    df = pd.DataFrame(df).sort_values(
        by=['coupling_length', 'gait_index', 'duty_cycle']
    )

    if row_filter is not None:
        df['keep'] = df.apply(row_filter, axis=1)
        df = df[df.keep]
        df.drop('keep', 1)

        keep_trial_ids = df['id'].tolist()
        keep_trials = []

        for trial in trials:
            if trial['id'] in keep_trial_ids:
                keep_trials.append(trial)
        trials = keep_trials

    df['order'] = np.arange(0, df.shape[0], 1)
    df['relative_uncertainty'] = df.uncertainty / df.coupling_length

    return dict(
        trials=trials,
        groups=groups,
        df=df
    )


def redundant_filter(row):
    """

    :param row:
    :return:
    """

    if row.gait_index in [0, 4] and row.duty_cycle > 50:
        # Remove trots and paces with DC > 50% because they are duplicates
        return False

    if row.duty_cycle > 60 and row.gait_index in [1, 2, 5, 6]:
        # Remove with DC > 0.5 because they are duplicates
        return False

    if row.gait_index == 7 and row.separation == 0:
        # Remove the smallest solutions because they are not physically
        # reasonable
        return False

    return True
