import measurement_stats as mstats
from tracksim.reporting import plotting

create = plotting.make_line_data


def coupling(trial):
    """
    :param trial:
    :return:
    """

    data = trial['couplings']['lengths']
    couplings = mstats.values.from_serialized([v['value'] for v in data])
    y, unc = mstats.values.unzip(couplings)
    gait_index = int(trial['id'][1])

    return plotting.make_line_data(
        x=[v['time'] for v in data],
        y=y,
        y_unc=unc,
        color=plotting.get_color(gait_index, 0.8, as_string=True),
        fill_color=plotting.get_color(gait_index, 0.3, as_string=True)
    )



