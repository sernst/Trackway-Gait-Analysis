import os
import typing

MY_PATH = os.path.abspath(os.path.dirname(__file__))

from tracksim import system

_path_overrides = dict()


def override(key: str, path: str):
    """

    :param key:
    :param path:
    :return:
    """

    if path is None:
        if key in _path_overrides:
            del _path_overrides[key]
        return

    _path_overrides[key] = clean(path)


def clean(path: str) -> str:
    """
    Cleans the specified path by expanding shorthand elements, redirecting to
    the real path for symbolic links, and removing any relative components to
    return a complete, absolute path to the specified location.

    :param path:
        The source path to be cleaned
    """

    if not path or path == '.':
        path = os.curdir()

    if path.startswith('~'):
        path = os.path.expanduser(path)

    return os.path.realpath(os.path.abspath(path))


def project(
        *args: typing.List[str],
        configs_override: str = None
) -> str:
    """
    Creates an absolute path to a file or folder within the trackway gait
    analysis project using the relative path elements specified by the args.

    :param args:
        Zero or more relative path elements that describe a file or folder
        within the project

    :param configs_override:
        An optional key within the tracksim configuration file where an
        override path can be supplied. If omitted, the path will default to the
        internal location within the source project
    """

    if configs_override:
        path = system.load_configs().get(configs_override)
        if path is not None:
            return clean(os.path.join(path, *args))

    return clean(os.path.join(MY_PATH, '..', *args))


def resource(
        *args: typing.List[str],
        use_configs: bool = True
) -> str:
    """
    Creates an absolute path to a file or folder within the resources folder of
    the trackway gait analysis project using the relative path elements
    specified by the args.

    :param args:
        Zero or more relative path elements that describe a file or folder
        within the resources folder
    :param use_configs:
        Specifies whether or not to use tracksim configuration settings that
        override the default path location
    """

    return project(
        'resources', *args,
        configs_override='path.resources' if use_configs else None
    )


def analysis(
        *args: typing.List[str],
        use_configs: bool = True
):
    """
    Creates an absolute path to a file or folder within the analysis folder of
    the trackway gait analysis project using the relative path elements
    specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the results folder
    :param use_configs:
        Specifies whether or not to use tracksim configuration settings that
        override the default path location
    """

    return project(
        'analysis', *args,
        configs_override='path.analysis' if use_configs else None
    )


def results(
        *args: typing.List[str],
        use_configs: bool = True
) -> str:
    """
    Creates an absolute path to a file or folder within the results folder of
    the trackway gait analysis project using the relative path elements
    specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the results folder
    :param use_configs:
        Specifies whether or not to use tracksim configuration settings that
        override the default path location
    """

    if 'results' in _path_overrides:
        return os.path.join(_path_overrides['results'], *args)

    return project(
        'results', *args,
        configs_override='path.results' if use_configs else None
    )
