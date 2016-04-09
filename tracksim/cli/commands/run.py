import functools
import json
import os
import sys
import typing
from argparse import ArgumentParser
from json import decoder as json_decoder

import tracksim
from tracksim import cli
from tracksim.group import simulate as simulate_group
from tracksim.trial import simulate as simulate_trial

DESCRIPTION = """
    Runs a trackway gait analysis simulation for the given scenario group
    or trial according to the path configuration options specified by the
    arguments
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

    paths = cli_configs.get('paths', []) + []
    paths.insert(0, os.getcwd())

    for directory in paths:
        p = os.path.abspath(os.path.join(directory, path))
        if os.path.exists(p):
            return p

    return None


def find_group_files(path: str) -> typing.List[str]:
    """
    Finds all group configuration JSON files stored in the specified path
    directory

    :param path:
        Path to the directory where the group files search should take place
    """

    paths = []

    # Prioritize group files named "group.json" over other files in the path
    items = ['group.json']
    for item in os.listdir(path):
        if item == 'group.json':
            continue
        items.append(item)

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
            paths.append(item_path)

    if not paths:
        tracksim.log('ERROR: No group trial found in path: "{}"'.format(path))
        tracksim.end(2)

    return paths

def run(**kwargs):
    """

    :param kwargs:
    :return:
    """

    cli_configs = kwargs.get('configs')
    if cli_configs is None:
        cli_configs = cli.load_configs()

    path = get_path(kwargs.get('path'), cli_configs)
    if path is None:
        tracksim.log('ERROR: Invalid or missing path argument')
        sys.exit(1)

    if os.path.isfile(path):
        with open(path, 'r+') as f:
            data = json.load(f)

        if bool('trials' in data):
            run_group(cli_configs, path, **kwargs)
        else:
            run_trial(cli_configs, path, **kwargs)
    else:
        group_paths = find_group_files(path)
        if not kwargs.get('run_all_groups'):
            group_paths = group_paths[0:1]

        urls = []
        for p in group_paths:
            results, url = run_group(cli_configs, p, **kwargs)
            urls.append(url)

        if len(urls) > 1:
            tracksim.log('Groups Run:', whitespace_top=2)
            for url in urls:
                tracksim.log(url)


def run_trial(cli_configs: dict, run_path: str, **kwargs) -> dict:
    """

    :param cli_configs:
    :param run_path:
    :param kwargs:
    :return:
    """

    tracksim.log('[START]: Trial Simulation')
    results = simulate_trial.run(
        run_path,
        report_path=kwargs.get('report_path')
    )
    tracksim.log('[COMPLETE]: Trial Simulation')

    url = finalize_run(cli_configs, results, is_group=False, **kwargs)

    return results, url


def run_group(cli_configs: dict, run_path: str, **kwargs) -> dict:
    """

    :param cli_configs:
    :param run_path:
    :param kwargs:
    :return:
    """

    def print_status(state, trial_configs, *args, **kwargs):
        message = 'Trial "{}"'.format(trial_configs['name'])
        tracksim.log('[{state}]: {message}'.format(
            state=state,
            message=message
        ))

    tracksim.log('[START]: Group Simulation')
    results = simulate_group.run(
        run_path,
        start_time=kwargs.get('start_time', 0),
        stop_time=kwargs.get('stop_time', 1.0e8),
        on_trial_start=functools.partial(print_status, 'START'),
        on_trial_complete=functools.partial(print_status, 'COMPLETE'),
        report_path=kwargs.get('report_path')
    )

    tracksim.log('[COMPLETE]: Group Simulation')

    url = finalize_run(cli_configs, results, is_group=True, **kwargs)

    return results, url


def finalize_run(
        cli_configs: dict,
        results: dict,
        is_group: bool,
        **kwargs
):
    """

    :param cli_configs:
    :param results:
    :param is_group:
    :param kwargs:
    :return:
    """

    tracksim.log('[FINALIZING]: Updating configuration and history')

    p = kwargs.get('path')
    if p:
        recent_paths = cli_configs.get('recent', [])
        recent_paths = list(filter((p).__ne__, recent_paths))
        recent_paths.insert(0, p)
        cli_configs['recent'] = recent_paths[:5]
        cli.save_configs(cli_configs)

    url = 'file://{}/{}.html?id={}'.format(
        results['report']['root_path'],
        'group' if is_group else 'trial',
        results['report']['id']
    )
    tracksim.log('[COMPLETE]: Simulation Done', URL=url)

    return url


def execute_command():
    """

    :return:
    """

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

    parser.add_argument(
        '-a', '--all',
        dest='run_all_groups',
        action='store_true',
        default=False,
        help=cli.reformat("""
            When included, this flag indicates that all of the group files
            within the specified path directory should be run in order,
            instead of just the first one found, which is the default behavior.
            """)
    )

    run(**vars(parser.parse_args()))



