from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
from json import encoder
import textwrap

def write_javascript_files(directory, sim_id, key, data):
    """

    :param directory:
    :param sim_id:
    :param key:
    :param data:
    :return:
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

    paths = []

    # Forces float rounding to behave so we don't end up with 1.20000000001
    # instead of 1.2
    storage = encoder.FLOAT_REPR
    encoder.FLOAT_REPR = lambda o: format(o, '%.12g')
    out = json.dumps(data)
    encoder.FLOAT_REPR = storage

    path = os.path.join(directory, '{}.json'.format(sim_id))
    with open(path, 'w+') as f:
        f.write(out)
    paths.append(path)

    contents = ("""
        (function () {
            'use strict';

            window.###KEY### = ###DATA###;
        }());
    """
        .replace('###KEY###', key)
        .replace('###DATA###', out) )

    contents = textwrap.dedent(contents).strip()
    path = os.path.join(directory, '{}.js'.format(sim_id))
    with open(path, 'w+') as f:
        f.write(contents)
    paths.append(path)

    return paths
