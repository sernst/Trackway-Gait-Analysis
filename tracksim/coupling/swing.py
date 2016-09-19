import math
import typing
import measurement_stats as mstats

WINDOW_SIZE = 2


def average_coupling_lengths(trial):
    """
    Calculate the average coupling lengths at each data sample in the trial
    using globally specified WINDOW_SIZE.

    :param trial:
    :return:
        A list of averaged coupling lengths for the specified trial
    """

    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )
    weighted = []
    unweighted = []

    for index in range(len(couplings)):
        segment = couplings[index:index + WINDOW_SIZE]
        if len(segment) < WINDOW_SIZE:
            break

        wxs = 0.0
        ws = 0.0
        for v in segment:
            w = 1.0 / (v.raw_uncertainty ** 2)
            wxs += w * v.raw
            ws += w

        weighted.append(mstats.ValueUncertainty(
            wxs / ws,
            1.0 / math.sqrt(ws)
        ))

        unweighted.append(sum(segment) / len(segment))

    return weighted, unweighted


def compute_many(
        trials: typing.List[dict]
) -> typing.Dict[str, mstats.ValueUncertainty]:
    """

    :param trials:
    :return:
    """

    swing = dict()
    swing.update([(trial['id'], compute(trial)) for trial in trials])
    return swing


def compute(trial) -> mstats.ValueUncertainty:
    """
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    weighted, unweighted = average_coupling_lengths(trial)

    max_cl = weighted[0]
    min_cl = weighted[0]
    for cl in weighted[1:]:
        max_cl = mstats.value.maximum(max_cl, cl)
        min_cl = mstats.value.minimum(min_cl, cl)

    s = abs(max_cl - min_cl) / median.value
    s.freeze()

    return s


def to_fitness(data: typing.Dict[str, mstats.ValueUncertainty]) -> dict:
    """

    :param data:
    :return:
    """

    fitness_values = dict()
    minimum_swing = mstats.values.minimum(data.values())

    for trial_id, res in data.items():
        fitness_values[trial_id] = abs(
            (res.value - minimum_swing.value) /
            math.sqrt(res.uncertainty ** 2 + minimum_swing.uncertainty ** 2)
        )

    max_value = max(fitness_values.values())

    out = dict()
    out.update([(tid, f / max_value) for tid, f in fitness_values.items()])
    return out
