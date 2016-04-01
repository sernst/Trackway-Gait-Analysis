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
        log([
            '[ERROR]: Failed to decode json file',
            [   'PATH: {}'.format(path),
                'INFO: {}'.format(err.msg),
                [   'LINE: {}'.format(err.lineno),
                    'CHAR: {}'.format(err.colno) ]]
        ])
        return end(1)

def save_configs(data):
    """

    :param data:
    :return:
    """

    path = os.path.expanduser('~/.tracksim.configs')
    with open(path, 'w+') as f:
        json.dump(data, f)


