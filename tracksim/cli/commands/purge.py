import os
import shutil

from tracksim import system
from tracksim import paths
from tracksim.cli import query

DESCRIPTION = """
    Lists all available reports in the results directories
    """


def execute_command():
    """

    :return:
    """

    system.log("""
        ==============
        REMOVE RESULTS
        ==============

        This command will remove all analysis, group and trial reports stored
        located in the directory:

        {}
        """.format(paths.results()), whitespace_bottom=1)

    do_it = query.confirm(
        'Are you sure you want to continue',
        default=False
    )

    if not do_it:
        system.log('[ABORTED]: No files were deleted')
        return system.end(0)

    path = paths.results('reports')

    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception:
            try:
                shutil.rmtree(path)
            except Exception:
                pass

    system.log("""
        [SUCCESS]: All results have been removed
        """, whitespace_top=1)


