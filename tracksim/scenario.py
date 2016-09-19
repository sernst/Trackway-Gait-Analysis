import os
import json
import shutil

from tracksim import paths


def create(**kwargs):
    """

    :param kwargs:
    :return:
    """

    if not kwargs.get('trackway_name'):
        raise ValueError('Missing trackway name')

    if not kwargs.get('scenario_name'):
        raise ValueError('Missing scenario name')

    if not kwargs.get('data_filename'):
        raise ValueError('Missing data filename')

    if not kwargs.get('root_path'):
        kwargs['root_path'] = os.path.abspath(os.path.curdir)

    if not kwargs.get('steps_per_cycle'):
        kwargs['steps_per_cycle'] = 20

    if not kwargs.get('duty_cycle'):
        kwargs['duty_cycle'] = 0.6

    target_path = deploy_directory(**kwargs)
    setup_trials(target_path, **kwargs)


def deploy_directory(**kwargs):
    template_path = paths.resource("template")

    target_path = os.path.join(
        kwargs['root_path'],
        kwargs['trackway_name'],
        kwargs['scenario_name']
    )

    if os.path.exists(target_path):
        raise FileExistsError('Scenario already exists')

    trackway_path = os.path.dirname(target_path)

    # create the scenario folder
    if not os.path.exists(trackway_path):
        os.makedirs(trackway_path)

    # copy the template version for each of the default trials
    shutil.copytree(template_path, target_path)

    # get group.json file and set it up.
    print('path = {}'.format(target_path))
    group_path = os.path.join(target_path, "group.json")

    print('group_path is [{}]'.format(group_path))
    if not os.path.exists(group_path):
        raise FileNotFoundError('group.json file not found')

    with open(group_path, mode='r+') as f:
        d = json.load(f)

    # set up the group's name key
    d["name"] = '{}_{}'.format(kwargs['trackway_name'], kwargs['scenario_name'])

    # save the group.json file with 2-space indents
    with open(group_path, mode='w+') as f:
        json.dump(d, f, indent=2, sort_keys=True)

    return target_path


def setup_trials(target_path, **kwargs):
    for item in os.listdir(target_path):
        # just work on the trials
        if item == 'group.json' or not item.endswith('.json'):
            continue

        item_path = os.path.join(target_path, item)
        print(item_path)

        with open(item_path, mode='r+') as f:
            d = json.load(f)

        d["data"] = kwargs['data_filename']
        d["steps_per_cycle"] = kwargs['steps_per_cycle']
        d["duty_cycle"] = kwargs['duty_cycle']

        if kwargs.get('start_time') is not None:
            d['start_time'] = kwargs['start_time']
        elif kwargs.get('begin_cycle') is not None:
            d['start_time'] = kwargs['begin_cycle']

        if kwargs.get('end_time') is not None:
            d['end_time'] = kwargs['end_time']
        elif kwargs.get('end_cycle') is not None:
            d['end_time'] = kwargs['end_cycle']

        # build unique trial name key starting with the full
        # gaitname (e.g., G5-trottingAmble2).  Verbose, but clear.
        ga = item.split('.')[0]
        tn = kwargs['trackway_name']
        sn = kwargs['scenario_name']

        name = '{}_{}_{}'.format(ga, tn, sn)

        if kwargs.get('start_time'):
            st = kwargs['start_time']
            d["start_time"] = st

        if kwargs.get('end_time'):
            et = kwargs['end_time']
            d["end_time"] = et

        print(name)
        d["name"] = name
        # save with 2-space indents
        with open(item_path, mode='w+') as f:
            json.dump(d, f, indent=2, sort_keys=True)

