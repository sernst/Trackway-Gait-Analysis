
import os
import stat

import tracksim
from tracksim import cli

DESCRIPTION = """
    Adds a tracksim script file to /usr/local/bin so that the tracksim cli
    can be executed globally
    """

def execute_command():

    source = tracksim.make_resource_path('tracksim.global.sh')

    with open(source, 'r+') as f:
        contents = f.read()

    path = tracksim.make_project_path('bin', 'tracksim')
    contents = contents.replace('###TRACKSIM_PATH###', path)

    path = '/usr/local/bin/tracksim'
    with open(path, 'w+') as f:
        f.write(contents)

    os.chmod(
        path,
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
        stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
        stat.S_IROTH | stat.S_IXOTH
    )

    tracksim.log("""
        [SUCCESS]: The tracksim command has been registered for global use. You
        can now call tracksim globally from a terminal.

        If you have trouble calling tracksim, make sure you have exported
            /usr/local/bin
        in your .bash_profile PATH.
        """)
