from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

import os
import json

def load(source, **kwargs):
    """ Loads a JSON configuration file from the specified source path if the
        source argument is a string. Otherwise, assumes the source is already
        a dictionary object with the configuration information.

        Then any specified keyword arguments are added to the configurations,
        replacing any keys that were already defined.

    :param source: Either a string representing an absolute path to the configs
        JSON file to be loaded, or a dictionary object of configuration values.

    :return: The loaded configuration dictionary object augmented by any
        keyword arguments.
    :rtype: dict
    """

    if isinstance(source, (six.string_types, six.binary_type)):
        path = source
        with open(path, 'r+') as f:
            source = json.load(f)
        source['path'] = os.path.dirname(path)
        source['filename'] = os.path.abspath(path)

    for k, v in kwargs.items():
        source[k] = v

    return source





