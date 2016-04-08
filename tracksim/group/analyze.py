import typing

def coupling_distribution_data(trial_results: typing.List[dict]) -> dict:
    """
    Bundles the coupling distribution data values for each of the trials

    :param trial_results:
        A list of simulation results dictionaries for each trial run in the
        group
    """

    data = [t['results']['couplings'] for t in trial_results]
    values = [x['value'] for x in data]

    return dict(values=values)
