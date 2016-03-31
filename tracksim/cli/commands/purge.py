import os
import shutil

import tracksim
from tracksim import cli
from tracksim.cli import query

DESCRIPTION = """
    Removes all existing group and trial results from cached results folders.
    """

def execute_command():

    do_it = query.confirm(
        'Remove all existing results files',
        default=False
    )

    if not do_it:
        cli.log('[ABORTED]: No files were deleted')
        return cli.end(0)

    path = tracksim.make_results_path('report', 'groups')
    if os.path.exists(path):
        shutil.rmtree(path)

    path = tracksim.make_results_path('report', 'trials')
    if os.path.exists(path):
        shutil.rmtree(path)


    cli.log("""
        [SUCCESS]: All group and trial results files have been removed
        """)

