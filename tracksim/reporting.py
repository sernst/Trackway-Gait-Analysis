import json
import os
import shutil
import textwrap
from json import encoder

import tracksim


def write_javascript_files(
        directory: str,
        sim_id: str,
        key: str,
        data: dict
) -> list:
    """
    Writes javascript files, both JSON file and JS files, containing the
    serialized data object in the specified directory

    :param directory:
        The path to a folder where the javascript files will be written
    :param sim_id:
        The file-safe simulation identifier that will be used as the file
        names for the written javascript files
    :param key:
        The variable name for the data object in the JavaScript (js) file,
        such that when loaded the data will be accessible on the window object
        with that key name. For example, if the key was 'DATA' then the
        JavaScript file would assign the data object to window.DATA
    :param data:
        The object to be serialized and written to the JSON and JS files
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

    paths = []

    # Forces float rounding to behave so we don't end up with 1.20000000001
    # instead of 1.2
    storage = encoder.FLOAT_REPR
    encoder.FLOAT_REPR = lambda o: format(o, '%.12g')
    out = json.dumps(data)
    encoder.FLOAT_REPR = storage

    path = os.path.join(directory, '{}.json'.format(sim_id))
    with open(path, 'w+') as f:
        f.write(out)
    paths.append(path)

    contents = ("""
        (function () {
            'use strict';

            window.###KEY### = ###DATA###;
        }());
    """
        .replace('###KEY###', key)
        .replace('###DATA###', out)
    )

    contents = textwrap.dedent(contents).strip()
    path = os.path.join(directory, '{}.js'.format(sim_id))
    with open(path, 'w+') as f:
        f.write(contents)
    paths.append(path)

    return paths


def save_temp_json_file(filename: str, data: dict):
    """
    Saves the data dictionary to a temporary JSON file with the specified
    filename

    :param filename:
        The name of the temp file to save. The filename can also contain folder
        components, representing a path relative to the temporary root path
        for the running tracksim application
    :param data:
        The data to be stored in the temp file
    """

    temp_path = tracksim.make_results_path('temp', filename)
    temp_folder = os.path.dirname(temp_path)
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

def initialize_output_directory(path: str = None) -> str:
    """
    Initializes the output directory where report files will be written for
    the trial or trials currently being run

    :param path:
        The path to the output directory that should be initialized for
        storing the report files for this instance of the tracksim application
    """

    if not path:
        # If the path is empty, the default internal_report_path will be used
        return tracksim.make_results_path('report')

    internal_report_path = tracksim.make_results_path('report')

    if path.startswith(internal_report_path):
        # Don't do any initialization if the path is the same as the default
        # internal report path where the source files already reside
        return tracksim.make_results_path('report')

    if not os.path.exists(path):
        os.makedirs(path)

    for item in os.listdir(internal_report_path):
        if item in ['groups', 'trials']:
            continue

        source_path = os.path.join(internal_report_path, item)
        dest_path = os.path.join(path, item)

        if os.path.isfile(source_path):
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.copy2(source_path, dest_path)
        else:
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)

    return path
