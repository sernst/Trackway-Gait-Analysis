import math
import measurement_stats as mstats


def compute_many(trials) -> dict:
    """

    :param trials:
    :return:
    """

    prss = dict()
    prss_norm = dict()

    for trial in trials:
        result = compute(trial)
        prss[trial['id']] = result['prss']
        prss_norm[trial['id']] = result['prss_norm']

    return dict(
        prss=prss,
        prss_norm=prss_norm
    )


def compute(trial) -> dict:
    """
    Calculates the persistence residual values for a given trial

    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )

    # Unnormalized
    residuals = [abs(cl - median.value) for cl in couplings]

    prss = mstats.ValueUncertainty(0, 0.0000001)
    for index, residual in enumerate(residuals[:-1]):
        prss += residual * residuals[index + 1]

    prss.freeze()

    # Normalized
    residuals = [abs(cl / median.value - 1) for cl in couplings]

    prss_norm = mstats.ValueUncertainty(0, 0.0000001)
    for index, residual in enumerate(residuals[:-1]):
        prss_norm += residual * residuals[index + 1]

    prss_norm /= len(residuals) - 1
    prss_norm.freeze()

    return dict(
        prss=prss,
        prss_norm=prss_norm
    )


def to_fitness(prss_data: dict) -> dict:
    """

    :param prss_data:
    :return:
    """

    data = prss_data['prss_norm'] if 'prss_norm' in prss_data else prss_data

    fitness_values = dict()
    minimum_residual = mstats.values.minimum(data.values())

    for track_id, res in data.items():
        fitness_values[track_id] = abs(
            (res.value - minimum_residual.value) /
            math.sqrt(res.uncertainty ** 2 + minimum_residual.uncertainty ** 2)
        )

    max_value = max(fitness_values.values())

    out = dict()
    out.update([(tid, f / max_value) for tid, f in fitness_values.items()])
    return out

