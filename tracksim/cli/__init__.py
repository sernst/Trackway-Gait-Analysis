import json
import os
import sys
from json import decoder as json_decoder
from textwrap import dedent

import tracksim


def reformat(source: str) -> str:
    """
    Formats the source string to strip newlines on both ends and dedents the
    the entire string

    :param source:
        The string to reformat
    """

    return dedent(source.strip('\n')).strip()

def fetch_command():
    """

    :return:
    """

    cmd = None
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

    if cmd in ['-h', '-help', '--help', '--h']:
        return 'help'

    if cmd is None or cmd.startswith('-'):
        tracksim.log("""
        [ERROR]: tracksim requires a command argument that defines the
        operation to be carried out. The expected structure is:

            $ tracksim [COMMAND] [ARGUMENTS] [--OPTIONS]

        For a list of available commands run:

            $ tracksim help
        """)

        tracksim.end(1)

    return cmd
