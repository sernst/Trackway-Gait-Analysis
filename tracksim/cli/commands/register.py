import os
import stat

from tracksim import system
from tracksim import paths

DESCRIPTION = """
    Adds a tracksim script file to /usr/local/bin so that the tracksim cli
    can be executed globally
    """

def register_global_var():
    """

    :return:
    """

    path = os.path.expanduser('~/.bash_profile')

    with open(path, 'r+') as f:
        lines = f.read().split('\n')

    entry = 'export TRACKSIM_HOME="{}"'.format(
        paths.project()
    )

    found_existing = False
    for index in range(len(lines)):
        l = lines[index]
        if l.startswith('export TRACKSIM_HOME='):
            if l == entry:
                return

            found_existing = True
            lines[index] = entry
            break

    if not found_existing:
        if len(lines[-1].strip()) < 1:
            lines.append('')
        lines.append('# Added by Tracksim gait analysis command')
        lines.append(entry)

    with open(path, 'w+') as f:
        f.write('\n'.join(lines))


def execute_command():

    source = paths.resource('tracksim.global.sh')

    with open(source, 'r+') as f:
        contents = f.read()

    path = paths.project('bin', 'tracksim')
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

    register_global_var()

    system.log("""
        [SUCCESS]: The tracksim command has been registered for global use. You
        can now call tracksim globally from a terminal.

        If you have trouble calling tracksim, make sure you have exported
            /usr/local/bin
        in your .bash_profile PATH.
        """)
