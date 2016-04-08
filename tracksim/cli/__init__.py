import json
import os
from json import decoder as json_decoder
from textwrap import dedent

import tracksim

def reformat(source: str) -> str:
    """
    Formats the source string to strip newlines on both ends and dedents the
    the entire string

    :param source:
        The string to reformat
    """

    return dedent(source.strip('\n')).strip()

def load_configs() -> dict:
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
        tracksim.log([
            '[ERROR]: Failed to decode json file',
            [   'PATH: {}'.format(path),
                'INFO: {}'.format(err.msg),
                [   'LINE: {}'.format(err.lineno),
                    'CHAR: {}'.format(err.colno) ]]
        ])
        return tracksim.end(1)

def save_configs(data: dict):
    """

    :param data:
    :return:
    """

    path = os.path.expanduser('~/.tracksim.configs')
    with open(path, 'w+') as f:
        json.dump(data, f)


