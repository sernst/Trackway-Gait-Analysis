from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import measurement_stats as mstats

def distance_between(p1, p2):
    """

    :param p1:
    :param p2:
    :return:
    """

    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if mstats.value.equivalent(dx.value, 0.0):
        sum_for_error = dx + dy
        return mstats.value.ValueUncertainty(
            abs(dy.raw),
            sum_for_error.raw_uncertainty)

    if mstats.value.equivalent(dy.value, 0.0):
        sum_for_error = dx + dy
        return mstats.value.ValueUncertainty(
            abs(dx.raw),
            sum_for_error.raw_uncertainty)

    try:
        return (
            dx ** 2 +
            dy ** 2) ** 0.5
    except Exception as err:
        print('Positions:', p1, p2, err)
        raise
