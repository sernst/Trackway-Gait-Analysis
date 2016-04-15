import os
import shutil

import tracksim
from tracksim.cli import query

DESCRIPTION = """
    Removes all existing group and trial results from cached results folders
    """


def execute_command():
    """

    :return:
    """

    tracksim.log("""
        ==============
        REMOVE RESULTS
        ==============

        This command will remove all analysis, group and trial reports stored
        located in the directory:

        {}
        """.format(tracksim.make_results_path()), whitespace_bottom=1)

    do_it = query.confirm(
        'Are you sure you want to continue',
        default=False
    )

    if not do_it:
        tracksim.log('[ABORTED]: No files were deleted')
        return tracksim.end(0)

    folders = ['groups', 'trials', 'analysis']

    for folder in folders:
        path = tracksim.make_results_path(folder)

        if not os.path.exists(path):
            continue

        try:
            shutil.rmtree(path)
        except Exception:
            try:
                shutil.rmtree(path)
            except Exception:
                pass

    tracksim.log("""
        [SUCCESS]: All group, trial and analysis results files have been removed
        """, whitespace_top=1)

