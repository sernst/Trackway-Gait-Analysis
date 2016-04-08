import functools
import json
import os
import re
import sys
from argparse import ArgumentParser
from json import decoder as json_decoder

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

    paths = run_configs.get('paths', []) + []
    paths.insert(0, os.getcwd())

    for directory in paths:
        p = os.path.abspath(os.path.join(directory, path))
        if os.path.exists(p):
            return p

    return None


def find_group_file(path: str) -> str:
    """

    :param path:
    :return:
    """

    # Prioritize group files named "group.json" over other files in the path
    items = ['group.json'] + os.listdir(path)

    for item in items:
        item_path = os.path.join(path, item)
        if not os.path.exists(item_path):
            continue

        if not os.path.isfile(item_path) or not item.endswith('.json'):
            continue

        try:
            with open(item_path, 'r+') as f:
                data = json.load(f)
        except json_decoder.JSONDecodeError as err:
            tracksim.log([
                '[ERROR]: Failed to decode json file',
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

        if 'trials' in data:
            return item_path

    tracksim.log('ERROR: No group trial found in path: "{}"'.format(path))
    tracksim.end(2)


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
        tracksim.log('ERROR: Invalid or missing path argument')
        sys.exit(1)

    if os.path.isdir(path):
        is_trial = False
        path = find_group_file(path)
    else:
        with open(path, 'r+') as f:
            data = json.load(f)

        is_trial = bool('trials' in data)

    def print_status(state, trial_configs, *args, **kwargs):
        message = 'Trial "{}"'.format(trial_configs['name'])
        tracksim.log('[{state}]: {message}'.format(
            state=state,
            message=message
        ))

    if simulate_group:
        tracksim.log('[START]: Group Simulation')
        results = simulate_group.run(
            path,
            start_time=kwargs.get('start_time', 0),
            stop_time=kwargs.get('stop_time', 1.0e8),
            on_trial_start=functools.partial(print_status, 'START'),
            on_trial_complete=functools.partial(print_status, 'COMPLETE'),
            report_path=kwargs.get('report_path')
        )
    else:
        tracksim.log('[START]: Trial Simulation')
        results = simulate_trial.run(
            path,
            report_path=kwargs.get('report_path')
        )

    p = kwargs.get('path')
    if p:
        recent_paths = run_configs.get('recent', [])
        recent_paths = list(filter((p).__ne__, recent_paths))
        recent_paths.insert(0, p)
        run_configs['recent'] = recent_paths[:5]
        cli.save_configs(run_configs)

    url = 'file://{}/{}.html?id={}'.format(
        results['report']['root_path'],
        'trial' if is_trial else 'group',
        results['report']['id']
    )
    tracksim.log('[COMPLETE]: Simulation Done', URL=url)


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


def execute_command():
    """

    :return:
    """
    if len(sys.argv) < 3:
        return run_interactive()

    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'run',
        type=str,
        help='The run command to execute'
    )

    parser.add_argument(
        'path',
        type=str,
        help=cli.reformat("""
            The relative or absolute path to either a group or trial simulation
            configuration file, or a directory path in which a group trial
            configuration file resides.
            """)
    )

    parser.add_argument(
        '-st', '--startTime',
        dest='start_time',
        type=float,
        default=0.0,
        help=cli.reformat("""
            The time at which the simulation should start. The default value
            is 0.
            """)
    )

    parser.add_argument(
        '-et', '--endTime',
        dest='stop_time',
        type=float,
        default=1.0e8,
        help=cli.reformat("""
            The time at which the simulation should stop. The default value is
            to run until the end of the simulation.
            """)
    )

    parser.add_argument(
        '-d', '--directory',
        dest='report_path',
        type=str,
        default=None,
        help=cli.reformat("""
            An absolute path to the output directory where you would like the
            trial results stored. This overrides the output directory specified
            by the configure command or from within the trial or group
            configuration file.
            """)
    )

    run(**vars(parser.parse_args()))




