from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

MY_PATH = os.path.abspath(os.path.dirname(__file__))

def make_project_path(*args):
    """ Creates an absolute path to a file or folder within the trackway gait
        analysis project using the relative path elements specified by the
        args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the project

    :return: An absolute path to the given file or folder
    :rtype: basestring
    """

    return os.path.abspath(os.path.join(MY_PATH, '..', *args))

def make_resource_path(*args):
    """ Creates an absolute path to a file or folder within the resources
        folder of the trackway gait analysis project using the relative path
        elements specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the resources folder

    :return: An absolute path to the given file or folder
    :rtype: basestring
    """

    return make_project_path('resources', *args)

def make_results_path(*args):
    """ Creates an absolute path to a file or folder within the results
        folder of the trackway gait analysis project using the relative path
        elements specified by the args.

    :param args: Zero or more relative path elements that describe a file or
        folder within the results folder

    :return: An absolute path to the given file or folder
    """

    return make_project_path('results', *args)

