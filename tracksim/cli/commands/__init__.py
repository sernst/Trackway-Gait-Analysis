import sys

import tracksim
from tracksim import cli
from tracksim.cli.commands import run
from tracksim.cli.commands import register
from tracksim.cli.commands import deregister
from tracksim.cli.commands import deploy
from tracksim.cli.commands import purge
from tracksim.cli.commands import configure

ME = sys.modules[__name__]

def list_modules():

    for key in dir(ME):
        item = getattr(ME, key)
        if hasattr(item, 'DESCRIPTION'):
            print('')
            tracksim.log('[{}]:\n   {}'.format(
                key,
                cli.reformat(getattr(item, 'DESCRIPTION'))
                    .replace('\n', '\n   ')
            ))

def get_module(command):
    """

    :param command:
    :return:
    """

    if not hasattr(ME, command):
        return None

    return getattr(ME, command)

