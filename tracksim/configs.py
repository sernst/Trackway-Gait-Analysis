import json
import os
import typing
from json import decoder as json_decoder

from tracksim import system
from tracksim import limb


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
            system.log([
                '[ERROR]: No such configuration file',
                ['PATH: {}'.format(path)]
            ])
            return system.end(1)
        except json_decoder.JSONDecodeError as err:
            system.log([
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
            return system.end(1)

        source['filename'] = os.path.abspath(path)
        source['path'] = os.path.dirname(source['filename'])
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
) -> typing.List[float]:
    """

    :param activity_phases:
    :param duty_cycle:
    :return:
    """

    activity_phases = to_phases_list(activity_phases)
    out = []
    for ap in activity_phases:
        out.append(time_to_support_time(ap, duty_cycle))

    return out


def support_to_activity_phases(
        support_phases: typing.Union[dict, typing.Iterable],
        duty_cycle: float
) -> typing.List[float]:
    """

    :param support_phases:
    :param duty_cycle:
    :return:
    """

    support_phases = to_phases_list(support_phases)

    out = []
    for sp in support_phases:
        out.append(support_time_to_time(sp, duty_cycle))

    return out


def time_to_support_time(time: float, duty_cycle: float) -> float:
    """

    :param time:
    :param duty_cycle:
    :return:
    """

    return time - (1.0 - duty_cycle)


def support_time_to_time(support_time: float, duty_cycle: float) -> float:
    """

    :param support_time:
    :param duty_cycle:
    :return:
    """

    return support_time + (1.0 - duty_cycle)


def to_phases_list(
        source: typing.Union[list, tuple, dict]
) -> typing.List[float]:
    """

    :param source:
    :return:
    """

    if not isinstance(source, dict):
        return list(source)

    out = [0, 0, 0, 0]
    for index, key in enumerate(limb.KEYS):
        if key in source:
            out[index] = source[key]
    for index, key in enumerate(limb.SHORT_KEYS):
        if key in source:
            out[index] = source[key]
    return out
