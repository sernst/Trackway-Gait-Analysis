from argparse import ArgumentParser

from tracksim import cli
from tracksim import scenario

DESCRIPTION = \
    """
    Creates a new simulation scenario
    """


def run(**kwargs):
    pass


def execute_command():

    parser = ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        'create_command',
        help='The create command itself'
    )

    parser.add_argument(
        '-t', '--trackway',
        dest='trackway_name',
        type=str,
        default=None,
        help=cli.reformat("""
            The name of the trackway for the simulation
            """)
    )

    parser.add_argument(
        '-s', '--scenario',
        dest='scenario_name',
        type=str,
        default=None,
        help=cli.reformat("""
            The name of the simulation scenario
            """)
    )

    parser.add_argument(
        '-d', '--data',
        dest='data_filename',
        type=str,
        default=None,
        help=cli.reformat("""
            The name of the csv file
            """)
    )

    parser.add_argument(
        '-p', '--path',
        dest='root_path',
        type=str,
        default='.',
        help=cli.reformat("""
            The path to the root directory where this simulation will be
            created
            """)
    )

    parser.add_argument(
        '-c', '--cycle',
        dest='duty_cycle',
        type=float,
        default=0.6,
        help=cli.reformat("""
            The path to the root directory where this simulation will be
            created
            """)
    )

    parser.add_argument(
        '-f', '--frequency',
        dest='steps_per_cycle',
        type=int,
        default=20,
        help=cli.reformat("""
            The path to the root directory where this simulation will be
            created
            """)
    )

    parser.add_argument(
        '-b', '--begin-cycle',
        dest='begin_cycle',
        type=float,
        default=None,
        help='The cycle at which to start the simulation'
    )

    parser.add_argument(
        '-e', '--end-cycle',
        dest='end_cycle',
        type=float,
        default=None,
        help='The cycle at which to end the simulation'
    )

    kwargs = vars(parser.parse_args())
    scenario.create(**kwargs)
