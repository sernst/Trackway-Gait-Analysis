from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
from json import decoder as json_decoder

import six

from tracksim import cli


def load(source, inherits = None, **kwargs):
    """ Loads a JSON configuration file from the specified source path if the
        source argument is a string. Otherwise, assumes the source is already
        a dictionary object with the configuration information.

        Then any specified keyword arguments are added to the configurations,
        replacing any keys that were already defined.

    :param source: Either a string representing an absolute path to the configs
        JSON file to be loaded, or a dictionary object of configuration values.

    :param inherits:

    :return: The loaded configuration dictionary object augmented by any
        keyword arguments.
    :rtype: dict
    """

    if isinstance(source, (six.string_types, six.binary_type)):
        path = source

        try:
            with open(path, 'r+') as f:
                source = json.load(f)
        except FileNotFoundError as err:
            print('[ERROR]: No such configuration file')
            print('  PATH:', path)
            return cli.end(1)
        except json_decoder.JSONDecodeError as err:
            print('[ERROR]: Failed to decode configs json file')
            print('  PATH:', path)
            print('  INFO:', err.msg)
            print('    LINE:', err.lineno)
            print('    CHAR:', err.colno)
            return cli.end(1)

        source['path'] = os.path.dirname(path)
        source['filename'] = os.path.abspath(path)

    if inherits:
        for k, v in inherits.items():
            if k not in source:
                source[k] = v

    for k, v in kwargs.items():
        source[k] = v

    return source





