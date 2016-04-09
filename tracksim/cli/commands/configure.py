from argparse import ArgumentParser

import tracksim
from tracksim import cli

DESCRIPTION = """
    Configures the tracksim command line settings
    """

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
        help=cli.reformat("""
            The configuration key to be modify
            """)
    )

    parser.add_argument(
        'value',
        type=str,
        help=cli.reformat("""
            The value to assign to the configuration key
            """)
    )

    args = vars(parser.parse_args())

    configs = cli.load_configs()
    configs[args['key']] = args['value']
    cli.save_configs(configs)

    tracksim.log(
        '[UPDATED]: Configuration setting "{}" updated'.format(args['key'])
    )
    tracksim.end(0)
