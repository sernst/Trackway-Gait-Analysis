import os
import sys
import typing
from argparse import ArgumentParser

from tracksim import cli
from tracksim import configs
from tracksim import system
from tracksim.trial import simulate

DESCRIPTION = """
    Generates a csv file for the specified group or trial
    """


def get_path(path: str, cli_configs: dict) -> typing.Union[str, None]:
    """

    :param path:
    :param cli_configs:
    :return:
    """

    if path.startswith('./'):
        path = os.path.abspath(path)

    if os.path.exists(path):
        return path

    config_paths = cli_configs.get('paths', []) + []
    config_paths.insert(0, os.getcwd())

    for directory in config_paths:
        p = os.path.abspath(os.path.join(directory, path))
        if os.path.exists(p):
            return p

    return None


def execute_command():
    """

    :return:
    """

    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'generate_command',
        type=str,
        help='The generate command itself'
    )

    parser.add_argument(
        'trial_or_group',
        type=str,
        help='Path to a trial or group file where the data source is specified'
    )

    parser.add_argument(
        'output_filename',
        type=str,
        help='Name of the csv file to be created'
    )

    args = parser.parse_args()
    cli_configs = system.load_configs()

    path = get_path(args.trial_or_group, cli_configs)
    if path is None:
        system.log('ERROR: Invalid or missing trial/group path')
        sys.exit(1)

    settings = configs.load(None, path)
    out_path = os.path.join(settings['directory'], args.output_filename)

    simulate.load_trackway_positions(
        settings,
        save_as=out_path
    )
