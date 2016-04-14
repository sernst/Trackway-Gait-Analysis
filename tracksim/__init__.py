import sys
import os
from textwrap import dedent
import typing
import json
from json import decoder as json_decoder


MY_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIGS = None

def make_project_path(*args: typing.List[str]) -> str:
    """
    Creates an absolute path to a file or folder within the trackway gait
    analysis project using the relative path elements specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the project
    """

    return os.path.abspath(os.path.join(MY_PATH, '..', *args))


def make_resource_path(*args: typing.List[str]) -> str:
    """
    Creates an absolute path to a file or folder within the resources folder of
    the trackway gait analysis project using the relative path elements
    specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the resources folder
    """

    return make_project_path('resources', *args)


def make_results_path(*args: typing.List[str]) -> str:
    """
    Creates an absolute path to a file or folder within the results folder of
    the trackway gait analysis project using the relative path elements
    specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the results folder
    """

    return make_project_path('results', *args)


def log(
        message: typing.Union[str, list],
        whitespace: int = 0,
        whitespace_top: int = 0,
        whitespace_bottom: int = 0,
        **kwargs
) -> str:
    """
    Logs a message to the console with the formatting support beyond a simple
    print statement or logger statement.

    :param message:
        The primary log message for the entry
    :param whitespace:
        The number of lines of whitespace to append to the beginning and end
        of the log message when printed to the console
    :param whitespace_top:
        The number of lines of whitespace to append to the beginning only of
        the log message when printed to the console. If whitespace_top and
        whitespace are both specified, the larger of the two values will be
        used.
    :param whitespace_bottom:
        The number of lines of whitespace to append to the end of the log
        message when printed to the console. If whitespace_bottom and
        whitespace are both specified, the larger of hte two values will be
        used.
    :param kwargs:
    """

    m = []

    def add_to_message(data, indent_level=0):
        """ Adds data to the message object """

        if isinstance(data, str):
            m.append('{}{}'.format(indent_level * '  ', data))
            return

        for line in data:
            if isinstance(line, str):
                add_to_message(line, indent_level)
            else:
                add_to_message(line, indent_level + 1)

    add_to_message(message)
    for key, value in kwargs.items():
        m.append('{key}: {value}'.format(key=key, value=value))

    message = dedent('\n'.join(m).strip('\n')).strip()

    pre_whitespace = int(max(whitespace, whitespace_top))
    post_whitespace = int(max(whitespace, whitespace_bottom))

    if pre_whitespace:
        print(pre_whitespace * '\n')
    print(message)
    if post_whitespace:
        print(post_whitespace * '\n')

    return message


def end(code: int):
    """
    Ends the application with the specified error code, adding whitespace to
    the end of the console log output for clarity

    :param code:
        The integer status code to apply on exit. If the value is non-zero,
        indicating an error, a message will be printed to the console to
        inform the user that the application exited in error
    """

    print('\n')
    if code != 0:
        log('Failed with status code: {}'.format(code), whitespace=1)
    sys.exit(code)


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
        log([
            '[ERROR]: Failed to decode json file',
            ['PATH: {}'.format(path),
             'INFO: {}'.format(err.msg),
             ['LINE: {}'.format(err.lineno),
              'CHAR: {}'.format(err.colno)]]
        ])
        return end(1)


def save_configs(data: dict):
    """

    :param data:
    :return:
    """

    path = os.path.expanduser('~/.tracksim.configs')
    with open(path, 'w+') as f:
        json.dump(data, f)
