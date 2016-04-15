import os
from argparse import ArgumentParser

import tracksim
from tracksim import cli
from tracksim.analysis import execute

DESCRIPTION = """
    Executes the specified multi-part analysis on reported results
    """


def list_all(analysis_path: str = None):

    if not analysis_path:
        analysis_path = tracksim.make_analysis_path()

    items = []
    for item in os.listdir(analysis_path):
        item_path = os.path.join(analysis_path, item)
        if not os.path.isdir(item_path):
            continue

        json_path = os.path.join(item_path, 'run.json')
        if not os.path.exists(json_path):
            continue

        items.append(item)

    if not items:
        tracksim.log('No analyses found at: {}'.format(analysis_path))
        return

    tracksim.log("""
        The following analyses are available:
          * {items}
        """.format(items='  * '.join(items)))


def execute_command():
    """

    :return:
    """

    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'analyze',
        type=str,
        help='The analyze command being executed'
    )

    parser.add_argument(
        'name',
        type=str,
        nargs='?',
        default=None,
        help=cli.reformat("""
            The identifier for the analysis, which is the same as its folder
            name within the analysis directory.
            """)
    )

    parser.add_argument(
        '-p', '--path',
        dest='analysis_path',
        type=str,
        help=cli.reformat("""
            The path to the analysis directory where the specified analysis
            resides. If not specified the default analysis directory, internal
            to the project will be used
            """)
    )

    parser.add_argument(
        '-l', '--list',
        dest='list',
        action='store_true',
        help=cli.reformat("""
            When specified, all of the available analyses in the current
            analysis path will be listed. Only valid when no analysis name is
            given.
            """)
    )

    args = vars(parser.parse_args())

    if not args['name']:
        if args['list']:
            list_all(args['analysis_path'])
        else:
            parser.print_help()
    else:
        execute.run(args['name'], args['analysis_path'])
