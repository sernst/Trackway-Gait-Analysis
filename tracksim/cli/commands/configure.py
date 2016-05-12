import typing
from argparse import ArgumentParser

from tracksim import system
from tracksim import paths
from tracksim import cli

DESCRIPTION = """
    Configures the tracksim command line settings
    """

def remove_key(configs: dict, key: str):
    """
    Removes the specified key from the tracksim configs if the key exists

    :param configs:
        The tracksim configs object to modify
    :param key:
        The key in the tracksim configs object to remove
    """

    if key in configs:
        del configs[key]
    system.save_configs(configs)
    system.log(
        '[REMOVED]: "{}" from configuration settings'.format(key)
    )


def set_key(configs: dict, key: str, value: typing.List[str]):
    """
    Removes the specified key from the tracksim configs if the key exists

    :param configs:
        The tracksim configs object to modify
    :param key:
        The key in the tracksim configs object to remove
    :param value:
    """

    if key.startswith('path.'):
        for index in range(len(value)):
            value[index] = paths.clean(value[index])

    if len(value) == 1:
        value = value[0]

    configs[key] = value
    system.save_configs(configs)
    system.log('[SET]: "{}" to "{}"'.format(key, value))


def echo_key(configs: dict, key: str):
    """

    :param configs:
    :param key:
    :return:
    """

    if key not in configs:
        system.log('[MISSING]: No "{}" key was found'.format(key))
        return

    system.log('[VALUE]: "{}" = {}'.format(key, configs[key]))


def echo_all(configs: dict):
    """

    :param configs:
    :return:
    """

    keys = list(configs.keys())
    keys.sort()
    out = ['Current Configuration:']
    for k in keys:
        out.append('  * {key}: {value}'.format(key=k, value=configs[k]))

    system.log('\n'.join(out))


def execute_command():
    """ Runs the configure command """

    parser = ArgumentParser()
    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'configure',
        type=str,
        help='The configure command to execute'
    )

    parser.add_argument(
        'key',
        type=str,
        nargs='?',
        default=None,
        help=cli.reformat("""
            The configuration key to be modify
            """)
    )

    parser.add_argument(
        'value',
        type=str,
        nargs='*',
        default=None,
        help=cli.reformat("""
            The value to assign to the configuration key. If omitted, the
            currently stored value for this key will be displayed.
            """)
    )

    parser.add_argument(
        '-r', '--remove',
        dest='remove',
        action='store_true',
        default=False,
        help=cli.reformat("""
            When included, this flag indicates that the specified key should
            be removed from the tracksim configs file.
            """)
    )

    parser.add_argument(
        '-l', '--list',
        dest='list',
        action='store_true',
        default=False,
        help=cli.reformat("""
            This flag is only useful when no key and no value have been
            specified. In such a case, this command will list all keys and
            values currently stored in the configuration file.
            """)
    )

    args = vars(parser.parse_args())

    configs = system.load_configs()
    if args['key'] is None:
        if args['list']:
            echo_all(configs)
        else:
            parser.print_help()
    elif len(args['value']) < 1:
        if args['remove']:
            remove_key(configs, args['key'])
        else:
            echo_key(configs, args['key'])
    else:
        set_key(configs, args['key'], args['value'])

    system.end(0)
