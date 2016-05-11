import json
import os
import typing
from json import decoder as json_decoder

import tracksim


def load(
        configs_type: str,
        source: typing.Union[str, dict],
        inherits: dict = None,
        **kwargs
) -> dict:
    """
    Loads a JSON configuration file from the specified source path if the source
    argument is a string. Otherwise, assumes the source is already a dictionary
    object with the configuration information.

    Then any specified keyword arguments are added to the configurations,
    replacing any keys that were already defined.

    :param configs_type:
        The enumerated type of the configurations to be loaded
    :param source:
        Either a string representing an absolute path to the configs JSON file
        to be loaded, or a dictionary object of configuration values
    :param inherits:
        An optional dictionary of values that should be inherited where they
        do not exist already in the source settings
    :return: The loaded configuration dictionary object augmented by any
        keyword arguments
    """

    c = configs_type[0].lower()
    if c == 't':
        configs_type = 'trial'
    elif c == 'g':
        configs_type = 'group'

    if isinstance(source, str):
        path = source

        try:
            with open(path, 'r+') as f:
                source = json.load(f)
        except FileNotFoundError:
            tracksim.log([
                '[ERROR]: No such configuration file',
                ['PATH: {}'.format(path)]
            ])
            return tracksim.end(1)
        except json_decoder.JSONDecodeError as err:
            tracksim.log([
                '[ERROR]: Failed to decode configs json file',
                [
                    'PATH: {}'.format(path),
                    'INFO: {}'.format(err.msg),
                    [
                        'LINE: {}'.format(err.lineno),
                        'CHAR: {}'.format(err.colno)
                    ]
                ]
            ])
            return tracksim.end(1)

        source['path'] = os.path.dirname(path)
        source['filename'] = os.path.abspath(path)

    else:
        source = json.loads(json.dumps(source))

    source['type'] = configs_type

    if inherits:
        for k, v in inherits.items():
            if configs_type == 'trial' and k in ['trials']:
                continue

            if k not in source:
                source[k] = v

    for k, v in kwargs.items():
        source[k] = v

    source['id'] = source['name'].replace(' ', '-')

    return source


def activity_to_support_phases(
        activity_phases: typing.Union[dict, typing.Iterable],
        duty_cycle: float
) -> typing.Iterable[float]:
    """

    :param activity_phases:
    :param duty_cycle:
    :return:
    """

    if isinstance(activity_phases, dict):
        out = dict()
        for key, value in activity_phases.items():
            out[key] = value - duty_cycle
        return out

    out = []
    for ap in activity_phases:
        out.append(ap - duty_cycle)
    return out


def support_to_activity_phases(
        support_phases: typing.Union[dict, typing.Iterable],
        duty_cycle: float
) -> typing.Iterable[float]:
    """

    :param support_phases:
    :param duty_cycle:
    :return:
    """

    if isinstance(support_phases, dict):
        out = dict()
        for key, value in support_phases.items():
            out[key] = value + duty_cycle
        return out

    out = []
    for sp in support_phases:
        out.append(sp + duty_cycle)
    return out

