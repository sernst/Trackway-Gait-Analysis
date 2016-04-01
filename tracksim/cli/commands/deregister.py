
import os

import tracksim
from tracksim import cli

DESCRIPTION = """
    Removes an existing tracksim script file at /usr/local/bin
    """

def execute_command():

    path = '/usr/local/bin/tracksim'
    if not os.path.exists(path):
        tracksim.log(cli.reformat("""
            [INFO]: The tracksim command was not registered. Operation aborted.
            """))
        return

    os.remove(path)

    tracksim.log("""
        [SUCCESS]: The tracksim command is no longer registered for global use.
        """)
