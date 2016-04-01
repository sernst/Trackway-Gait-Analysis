from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
from textwrap import dedent

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


def log(message, whitespace=0, whitespace_top=0, whitespace_bottom=0,
        **kwargs):
    """

    :param message:
    :param whitespace:
    :param whitespace_top:
    :param whitespace_bottom:
    :param kwargs:
    :return:
    """

    m = []


    def add_to_message(data, indent_level=0):
        if isinstance(data, str):
            m.append('{}{}'.format(indent_level * '  ', data))
            return

        for line in data:
            if isinstance(line, str):
                add_to_message(line, indent_level)
            else:
                add_to_message(line, indent_level + 1)


    add_to_message(message)
    for key, value in kwargs.items():
        m.append('{key}: {value}'.format(key=key, value=value))

    message = dedent('\n'.join(m).strip('\n')).strip()

    pre_whitespace = int(max(whitespace, whitespace_top))
    post_whitespace = int(max(whitespace, whitespace_bottom))

    if pre_whitespace:
        print(pre_whitespace * '\n')
    print(message)
    if post_whitespace:
        print(post_whitespace * '\n')

    return message

def end(code):
    """

    :param code:
    :return:
    """

    print('\n')
    if code != 0:
        log('Failed with status code: {}\n'.format(code))
    sys.exit(code)
