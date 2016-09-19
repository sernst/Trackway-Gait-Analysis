import pandas as pd
import typing
import measurement_stats as mstats


def per_trial(
        trials: typing.List[dict],
        df: pd.DataFrame,
        function,
        **kwargs
) -> list:
    """
    Calls the specified function on each trial in the specified
    data frame. The signature for the function is:

        function(data_frame_row, trial_data, **kwargs)

    :param trials:
    :param df:
    :param function:
    :return:
        A dictionary containing the returned values of each function
        where the keys are the ID of the trial on which the function was
        executed.
    """

    results = dict()

    trial_kwargs = dict()
    for index, row in df.iterrows():
        trial_id = row.id

        for key, value in kwargs.items():
            if key.startswith('_'):
                trial_kwargs[key[1:]] = value[trial_id]
            else:
                trial_kwargs[key] = value

        for trial in trials:
            if trial['id'] == trial_id:
                results[trial['id']] = function(row, trial, **trial_kwargs)

    return results


def coupling_statistics(trial: dict) -> dict:
    """

    :param trial:
    :return:
    """

    data = trial['couplings']['lengths']
    median = mstats.ValueUncertainty(**trial['couplings']['value'])

    couplings = mstats.values.from_serialized([v['value'] for v in data])
    min_value = mstats.values.minimum(couplings)
    max_value = mstats.values.maximum(couplings)
    delta = abs(min_value - max_value)
    deviation = abs(min_value.value - max_value.value) / delta.uncertainty

    return dict(
        min=min_value.html_label,
        median=median.html_label,
        max=max_value.html_label,
        deviation=0.01 * round(100 * deviation)
    )
