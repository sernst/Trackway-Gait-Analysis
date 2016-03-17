from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import re
import sys
from argparse import ArgumentParser

import tracksim
from tracksim import cli
from tracksim.group import simulate as simulate_group
from tracksim.trial import simulate as simulate_trial

DESCRIPTION = """
    Runs a trackway gait analysis simulation for the given scenario group
    or trial according to the path configuration options specified by the
    arguments.
    """

def get_path(path, run_configs):
    """

    :param path:
    :param run_configs:
    :return:
    """

    if path.startswith('./'):
        path = os.path.abspath(path)

    if os.path.exists(path):
        return path

    for directory in run_configs.get('paths', []):
        p = os.path.abspath(os.path.join(directory, path))
        if os.path.exists(p):
            return p

    return None

def find_group_file(path):
    """

    :param path:
    :return:
    """

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if not os.path.isfile(item_path) or not item.endswith('.json'):
            continue

        with open(item_path, 'r+') as f:
            data = json.load(f)

        if 'trials' in data:
            return item_path

    cli.log('ERROR: No group trial found in path: "{}"'.format(path))
    sys.exit(2)

def run(**kwargs):
    """

    :param kwargs:
    :return:
    """

    run_configs = kwargs.get('configs')
    if run_configs is None:
        run_configs = cli.load_configs()

    path = get_path(kwargs.get('path'), run_configs)
    if path is None:
        cli.log('ERROR: Invalid or missing path argument. Unable to simulate')
        sys.exit(1)

    if os.path.isdir(path):
        is_trial = False
        path = find_group_file(path)
    else:
        with open(path, 'r+') as f:
            data = json.load(f)

        is_trial = bool('trials' in data)

    simulate = simulate_trial if is_trial else simulate_group
    results = simulate.run(path)

    p = kwargs.get('path')
    if p:
        recent_paths = run_configs.get('recent', [])
        recent_paths = list(filter((p).__ne__, recent_paths))
        recent_paths.insert(0, p)
        run_configs['recent'] = recent_paths[:5]
        cli.save_configs(run_configs)

    url = 'file://{}/{}.html?id={}'.format(
        tracksim.make_results_path('report'),
        'trial' if is_trial else 'group',
        results['report']['id']
    )
    cli.log('[COMPLETE]: Simulation Done', URL=url)

def run_interactive():
    """

    :return:
    """

    configs = cli.load_configs()
    recent = configs.get('recent', [])

    if recent:
        print('\n\nChoose Source Path for Simulation:')
        for index in range(len(recent)):
            print('{}: {}'.format(index, recent[index]))
        print('Or enter a new path')
        path = input('Source Path:')

        pattern = re.compile('^[0-9]+&')
        if pattern.match(path):
            path = recent[int(path, 10)]
    else:
        path = input('Enter Source Path:')

    return run(path=path, configs=configs)

def from_command_line():
    """

    :return:
    """
    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'command',
        type=str,
        help='The cli command to execute')

    parser.add_argument(
        'path',
        type=str,
        help=cli.reformat("""
            The absolute path to either a group or trial simulation
            configuration file, or a directory path in which a group trial
            configuration file resides.
            """))

    run(**vars(parser.parse_args()))

def execute_command():
    """

    :return:
    """
    if len(sys.argv) < 3:
        run_interactive()
    else:
        from_command_line()






