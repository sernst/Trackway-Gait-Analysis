import math
import numpy as np
import measurement_stats as mstats
import functools
import pandas as pd


def compute_fitness_rankings(df):
    """

    :param df:
    :return:
    """

    fitness_values = []
    for index, row in df.iterrows():
        fitness_values.append(
            compute_fitness(row['swing'], row['persistence'])
        )

    worst = max(fitness_values)
    return [worst - v for v in fitness_values]


def compute_fitness(*fitness_values):
    """

    :param fitness_values:
    :return:
    """

    sum_squares = sum([v ** 2 for v in fitness_values])
    return math.sqrt(sum_squares) / math.sqrt(len(fitness_values))


def distribution(
        df: pd.DataFrame,
        segment_min: float = 0,
        segment_max: float = 100,
        scale_factor: float = 1.0
) -> dict:
    """

    :param df:
    :param segment_min:
    :param segment_max:
    :param scale_factor:
    :return:
    """

    measurements = mstats.values.join(
        df['coupling_length'].tolist(),
        df['uncertainty'].tolist()
    )

    dist = mstats.create_distribution(measurements)
    x_values = mstats.distributions.adaptive_range(dist, 4)
    y_values = dist.heighted_probabilities_at(x_values, df['fitness'])

    max_value = functools.reduce(
        lambda a, b: (a if a[1] > b[1] else b),
        zip(x_values, y_values),
        (0, 0)
    )

    points = [
        p for p in zip(x_values, y_values)
        if segment_min < p[0] < segment_max
        ]
    x_segment_values, y_segment_values = zip(*points)

    population = mstats.distributions.population(dist, 4096)
    population = [x for x in population if segment_min < x < segment_max]

    coupling_length = mstats.ValueUncertainty(
        np.median(population),
        mstats.distributions.weighted_median_average_deviation(population)
    )

    gaussian_fit = mstats.create_distribution([coupling_length])

    y_gauss_values = gaussian_fit.probabilities_at(x_values)
    y_gauss_values = [scale_factor * y for y in y_gauss_values]

    return dict(
        dist=dist,
        max=max_value,
        coupling_length=coupling_length,
        values=dict(
            x=x_values,
            y=y_values
        ),
        segment=dict(
            x=x_segment_values,
            y=y_segment_values
        ),
        gauss=dict(
            x=x_values,
            y=y_gauss_values
        )
    )



