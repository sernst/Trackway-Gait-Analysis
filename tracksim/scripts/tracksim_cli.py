#!/usr/bin/env python3

from tracksim import system
from tracksim import cli
from tracksim.cli import commands


def run():
    """

    :return:
    """

    # Add whitespace when the command is executed
    print('\n')

    cmd = cli.fetch_command()

    if cmd == 'help':
        commands.show_help()
        system.end(0)

    command_module = commands.get_module(cmd)
    if command_module:
        command_module.execute_command()
    else:
        system.log('[ERROR]: Unrecognized command "{}"'.format(cmd))
        commands.show_help()

    system.end(0)
