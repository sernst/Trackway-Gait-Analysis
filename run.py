from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import json
from argparse import ArgumentParser
from textwrap import dedent

from tracksim.group import simulate as simulate_group
from tracksim.trial import simulate as simulate_trial

def log(message, **kwargs):
    """

    :param message:
    :param kwargs:
    :return:
    """

    print(message)
    for key, value in kwargs.items():
        print('{}:'.format(key), value)

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

def run(**kwargs):
    """

    :param kwargs:
    :return:
    """

    path = kwargs.get('path')
    if not os.path.exists(path):
        log('ERROR: Invalid or missing path argument. Unable to simulate')
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
    print(results)

def run_interactive():
    """

    :return:
    """

    path = input('Enter Source Path:')
    return run(path=path)

def from_command_line():
    """

    :return:
    """

    def _clean(source):
        return dedent(source).strip()

    parser = ArgumentParser()

    parser.description = _clean("""
        Runs a trackway gait analysis simulation for the given scenario group
        or trial according to the path configuration options specified by the
        arguments.
        """)

    #---------------------------------------------------------------------------
    # Positional Arguments
    parser.add_argument(
        'path',
        type=str,
        default=None,
        help=_clean("""
            The absolute path to either a group or trial simulation
            configuration file, or a directory path in which a group trial
            configuration file resides.
            """))

    run(**vars(parser.parse_args()))

################################################################################
################################################################################

if __name__ == '__main__':
    if len(sys.argv) < 2:
        run_interactive()
    else:
        from_command_line()






