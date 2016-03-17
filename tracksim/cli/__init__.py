import os
import sys
import json
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

    with open(path, 'r+') as f:
        return json.load(f)

def save_configs(data):
    """

    :param data:
    :return:
    """

    path = os.path.expanduser('~/.tracksim.configs')
    with open(path, 'w+') as f:
        json.dump(data, f)

def exit(code):
    """

    :param code:
    :return:
    """

    print('\n\n')
    sys.exit(code)
