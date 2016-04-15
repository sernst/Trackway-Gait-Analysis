import os
import types
import json

import tracksim
from tracksim import analysis


def run_step(filename: str, analysis_id: str, root_path: str, settings: dict):
    """

    :param filename:
    :param analysis_id:
    :param root_path:
    :param settings:
    :return:
    """

    module = types.ModuleType(filename.split('.')[0])

    # setattr(module, )
    analysis.cacher.put(
        __analysis_id__=analysis_id,
        __step_id__=filename.split('.')[0],
        __analysis_path__=root_path,
        __analysis_settings__=settings
    )

    file_path = os.path.join(root_path, filename)
    with open(file_path, 'r+') as f:
        contents = f.read()

    exec(contents, module.__dict__)


def run(analysis_id: str, analysis_path: str = None, results_path: str = None):
    """

    :param analysis_id:
    :param analysis_path:
    :param results_path:
    :return:
    """

    if analysis_path is None:
        analysis_path = tracksim.make_analysis_path()

    run_path = os.path.join(analysis_path, analysis_id, 'run.json')
    with open(run_path, 'r+') as f:
        settings = json.load(f)

    for filename in settings['steps']:
        run_step(
            filename=filename,
            analysis_id=analysis_id,
            root_path=os.path.join(analysis_path, analysis_id),
            settings=settings
        )

    if results_path is None:
        results_path = analysis.make_results_path()

    return analysis.report.write_report(path=results_path)
