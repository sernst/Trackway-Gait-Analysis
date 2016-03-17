
import os

from tracksim import cli

DESCRIPTION = """
    Removes an existing tracksim script file at /usr/local/bin
    """

def execute_command():

    path = '/usr/local/bin/tracksim'
    if not os.path.exists(path):
        cli.log(cli.reformat("""
            [INFO]: The tracksim command was not registered. Operation aborted.
            """))
        return

    os.remove(path)

    cli.log("""
        [SUCCESS]: The tracksim command is no longer registered for global use.
        """)
