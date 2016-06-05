from argparse import ArgumentParser

from tracksim import system
from tracksim import reader
from tracksim import paths
from tracksim import cli

DESCRIPTION = """
    Removes all existing group and trial results from cached results folders
    """


def list_groups():
    system.log('===== GROUPS =====', whitespace_bottom=1)

    results_path = paths.results('group.html')

    for uid, data_path in reader.listings('group').items():
        url = 'file://{}?id={}'.format(results_path, uid)

        system.log(
            """
            --- {uid} ---
              {url}
            """.format(uid=uid, url=url),
            whitespace_bottom=1
        )


def list_trials():
    system.log('===== TRIALS =====', whitespace_bottom=1)

    results_path = paths.results('trials.html')

    for uid, data_path in reader.listings('trial').items():
        url = 'file://{}?id={}'.format(results_path, uid)

        system.log(
            """
            --- {uid} ---
              {url}
            """.format(uid=uid, url=url),
            whitespace_bottom=1
        )


def execute_command():
    """

    :return:
    """

    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'list_command',
        type=str,
        help='The list command itself'
    )

    parser.add_argument(
        'report_type',
        type=str,
        nargs='?',
        default=None,
        help='The type of report to list.'
    )

    args = vars(parser.parse_args())

    report_type = args['report_type']
    if not report_type:
        report_type = 'all'
    else:
        report_type = report_type.lower()

    print('')
    if report_type[0] == 'g':
        list_groups()
    elif report_type[0] == 't':
        list_trials()
    else:
        list_groups()
        print('')
        list_trials()

