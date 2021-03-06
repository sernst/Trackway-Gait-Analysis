import os
import shutil
from argparse import ArgumentParser

from tracksim import cli
from tracksim import paths
from tracksim import system
from tracksim.reporting import create_index_file

DESCRIPTION = """
    Copies all of the current reports into a separate folder for portable
    viewing, and creates an index.html file in the top-level folder for
    easier access to them all.
    """


def run(
        path: str,
        source_directory: str,
        directory_name: str,
        force: bool,
        **kwargs
):
    """

    :param path:
    :param source_directory:
    :param directory_name:
    :param force:
    :return:
    """

    target_path = os.path.join(os.path.abspath(path), directory_name)
    if os.path.exists(target_path):

        if not force:
            system.log("""
            [ABORTED EXPORT]
            A file or directory already exists at the specified path:

            {path}

            If you would like to replace the existing data at this path location
            either delete the existing data first, or run this command with the
            force flag.
            """.format(path=target_path))
            system.end(1)

        system.log('[REMOVING]: Existing directory {}'.format(target_path))
        try:
            shutil.rmtree(target_path)
        except OSError:
            try:
                # Give it a second
                shutil.rmtree(target_path)
            except OSError:
                system.log("""
                    [ABORTED EXPORT]
                    The existing directory could not be removed.
                    Unable to continue.
                    """)
                system.end(1)

    omit_html = kwargs.get('omit_html', False)
    omit_data = kwargs.get('omit_data', False)

    def list_ignores(src, names):
        """
        Creates a list of file names that should not be copied to the
        destination during the copytree operation.

        :param src:
            Source directory where the files originate
        :param names:
            A list of file names in the source directory to filter
        :return:
            A list of file names in the source directory that should NOT
            be copied to the destination path
        """

        ignored_names = []
        for name in names:
            if omit_html and not name.endswith('.json'):
                ignored_names.append(name)
            if omit_data and name.endswith('.json'):
                ignored_names.append(name)
        return ignored_names

    shutil.copytree(source_directory, target_path, ignore=list_ignores)

    result = create_index_file(source_directory, target_path)

    system.log("""
        [EXPORT COMPLETE]
        The export process was successful. All existing reports are now
        accessible through the index file:

         * {url}
        """.format(url=result['url']), whitespace=1)


def execute_command():
    """

    :return:
    """

    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'export',
        type=str,
        help='The export command to execute'
    )

    parser.add_argument(
        'path',
        type=str,
        help=cli.reformat("""
            The relative or absolute path to the location where the exported
            reports directory will be created
            """)
    )

    parser.add_argument(
        '-d', '--directory',
        dest='directory_name',
        type=str,
        default='reports',
        help=cli.reformat("""
            The name of the directory to be created to store the results
            """)
    )

    parser.add_argument(
        '-s', '--source',
        dest='source_directory',
        type=str,
        default=paths.results(),
        help=cli.reformat("""
            The source reports directory to be exported. This flag allows you
            to export results that are stored in locations other than the
            default report location
            """)
    )

    parser.add_argument(
        '-f', '--force',
        dest='force',
        action='store_true',
        default=False,
        help=cli.reformat("""
            When included, the export process will overwrite any existing data
            at the specified path and directory. It should only be used to
            replace an existing exported reports directory with newer data
            """)
    )

    parser.add_argument(
        '-od', '--omit-data',
        dest='omit_data',
        action='store_true',
        default=False,
        help=cli.reformat("""
            When included, the export process will skip all of the raw data
            files for each group and trial. These files are not necessary for
            viewing the reports. They exist for post-simulation analyses.
            """)
    )

    parser.add_argument(
        '-oh', '--omit-html',
        dest='omit_html',
        action='store_true',
        default=False,
        help=cli.reformat("""
            When included, the export process will skip all of the html viewing
            related files and only export the data files for each group and
            trial. This is useful if you want to share or store data for
            analysis.
            """)
    )

    run(**vars(parser.parse_args()))
