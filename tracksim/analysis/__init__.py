import os
import shutil

import tracksim
from tracksim.analysis import cacher
from tracksim.analysis import report


def initialize_path(path: str = None) -> str:
    """

    :param path:
    :return:
    """

    if not path:
        path = make_results_path()

    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception:
            try:
                shutil.rmtree(path)
            except Exception:
                return None

    os.makedirs(path)
    return path


def make_results_path(*args, configs_override: str = None) -> str:
    """

    :param args:
    :param configs_override:
    :return:
    """

    if configs_override:
        path = tracksim.load_configs().get(configs_override)
        if path:
            return tracksim.clean_path(os.path.join(path, *args))

    analysis_id = cacher.fetch('__analysis_id__')
    if analysis_id:
        args = list(args)
        args.insert(0, analysis_id)

    return tracksim.make_results_path('analysis', *args)

