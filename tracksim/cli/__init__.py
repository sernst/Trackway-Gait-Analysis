import os
import sys
import json
from json import decoder as json_decoder
from textwrap import dedent

def reformat(argument_description):
    """

    :param argument_description:
    :return:
    """
    return dedent(argument_description.strip('\n')).strip()

def log(message, **kwargs):
    """

    :param message:
    :param kwargs:
    :return:
    """

    print(reformat(message))
    for key, value in kwargs.items():
        print('{}:'.format(key), value)

def load_configs():
    """

    :return:
    """

    path = os.path.expanduser('~/.tracksim.configs')
    if not os.path.exists(path):
        return {}

    try:
        with open(path, 'r+') as f:
            return json.load(f)
    except json_decoder.JSONDecodeError as err:
        print('[ERROR]: Failed to decode json file')
        print('  PATH:', path)
        print('  INFO:', err.msg)
        print('    LINE:', err.lineno)
        print('    CHAR:', err.colno)
        return end(1)

def save_configs(data):
    """

    :param data:
    :return:
    """

    path = os.path.expanduser('~/.tracksim.configs')
    with open(path, 'w+') as f:
        json.dump(data, f)

def end(code):
    """

    :param code:
    :return:
    """

    print('\n')
    if code != 0:
        print('Execution failed with status code: {}\n'.format(code))
    sys.exit(code)
