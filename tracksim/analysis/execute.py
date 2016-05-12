import os
import types
import json

from tracksim import system
from tracksim import paths
from tracksim import analysis
from tracksim.reporting.report import Report


def run_step(filename: str, analysis_id: str, root_path: str, settings: dict):
    """

    :param filename:
    :param analysis_id:
    :param root_path:
    :param settings:
    :return:
    """

    file_path = os.path.join(root_path, filename)

    if filename.endswith('.md'):
        with open(file_path, 'r+') as f:
            analysis.report.add_markdown(f.read())
        return

    module = types.ModuleType(filename.split('.')[0])

    # setattr(module, )
    analysis.shared.put(__step_id__=filename.split('.')[0])

    with open(file_path, 'r+') as f:
        contents = f.read()

    try:
        exec(contents, module.__dict__)
    except Exception:
        system.log("""
            ERROR: Analysis failed during in "{filename}"
            """.format(filename=filename))
        raise


def run(analysis_id: str, analysis_path: str = None, results_path: str = None):
    """

    :param analysis_id:
    :param analysis_path:
    :param results_path:
    :return:
    """

    if analysis_path is None:
        analysis_path = paths.analysis()

    run_path = os.path.join(analysis_path, analysis_id, 'run.json')
    with open(run_path, 'r+') as f:
        settings = json.load(f)

    report = Report('analysis', analysis_id)
    analysis.report = report

    cache = analysis.SharedCache()
    analysis.shared = cache
    cache.put(
        __analysis_id__=analysis_id,
        __analysis_path__=analysis_path,
        __analysis_settings__=settings
    )

    for filename in settings['steps']:
        run_step(
            filename=filename,
            analysis_id=analysis_id,
            root_path=os.path.join(analysis_path, analysis_id),
            settings=settings
        )

    url = analysis.report.write(results_path=results_path)

    path = os.path.join(
        analysis.report.directory,
        '{}.json'.format(analysis_id)
    )

    settings['id'] = analysis_id
    settings['name'] = settings.get('name', analysis_id)
    with open(path, 'w+') as f:
        json.dump({
            'settings': settings
        }, f)

    return url

