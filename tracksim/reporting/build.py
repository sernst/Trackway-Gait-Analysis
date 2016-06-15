import json
import os
import typing


def create_index_file(source_directory: str, target_directory: str) -> dict:
    """

    :param source_directory:
    :param target_directory:
    :return:
    """

    source_path = os.path.join(source_directory, 'index.tmpl.html')
    with open(source_path, 'r+') as f:
        contents = f.read()

    data = json.dumps({
        'groups': get_report_info('group', target_directory),
        'trials': get_report_info('trial', target_directory),
        'analysis': get_report_info('analysis', target_directory)
    })

    contents = contents.replace('\'###DATA###\'', data)

    target_path = os.path.join(target_directory, 'index.html')
    with open(target_path, 'w+') as f:
        f.write(contents)

    return {
        'path': target_path,
        'url': 'file://{}'.format(target_path)
    }


def get_report_info(report_type: str, target_path: str) -> typing.List[dict]:
    """

    :param report_type:
    :param target_path:
    :return:
    """

    out = []

    rt = report_type.lower()
    if rt.startswith('t'):
        report_type = 'trial'
    elif rt.startswith('g'):
        report_type = 'group'
    else:
        report_type = 'analysis'

    directory = os.path.join(target_path, 'reports', report_type)

    if not os.path.exists(directory):
        return out

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if not os.path.isdir(item_path):
            continue

        json_path = os.path.join(item_path, '{}.json'.format(item))
        if not os.path.exists(json_path):
            continue

        with open(json_path, 'r+') as f:
            data = json.load(f)

        out.append({
            'id': item,
            'url': '{}.html?id={}'.format(report_type, item),
            'title': data['settings']['name'],
            'summary': data['settings']['summary']
        })

    return out
