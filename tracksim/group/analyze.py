from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def coupling_distribution_data(trials):
    """

    :param trials:
    :return:
    """

    data = [t['results']['couplings'] for t in trials]
    values = [x['value'] for x in data]

    return dict(
        values=values,

    )
