import os
import shutil

import tracksim
from tracksim import cli
from tracksim.cli import query

DESCRIPTION = """
    Removes all existing group and trial results from cached results folders
    """

def execute_command():

    do_it = query.confirm(
        'Remove all existing results files',
        default=False
    )

    if not do_it:
        tracksim.log('[ABORTED]: No files were deleted')
        return tracksim.end(0)

    path = tracksim.make_results_path('report', 'groups')
    if os.path.exists(path):
        shutil.rmtree(path)

    path = tracksim.make_results_path('report', 'trials')
    if os.path.exists(path):
        shutil.rmtree(path)


    tracksim.log("""
        [SUCCESS]: All group and trial results files have been removed
        """)

