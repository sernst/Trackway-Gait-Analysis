import sys
import os
import json
from json import decoder as json_decoder
import mimetypes

import boto3
import tracksim
from tracksim import cli

CONFIGS_PATH = tracksim.make_project_path('ops', 'configs.json')

if not os.path.exists(CONFIGS_PATH):
    raise FileNotFoundError('Missing configs.json file')

configs = None
try:
    with open(CONFIGS_PATH, 'r') as f:
        configs = json.load(f)
except json_decoder.JSONDecodeError as err:
    tracksim.log([
        '[ERROR]: Failed to decode configs json file',
        [   'PATH: {}'.format(CONFIGS_PATH),
            'INFO: {}'.format(err.msg),
            [   'LINE: {}'.format(err.lineno),
                'CHAR: {}'.format(err.colno)
            ]]
    ])
    tracksim.end(1)

boto3.setup_default_session(profile_name=configs.get('aws_profile'))

s3 = boto3.client('s3')

bucket_name = configs['results']['bucket_name']
key_prefix = configs['results']['key_prefix']

def upload_in_folder(root_path, *parts):
    """

    :param root_path:
    :param parts:
    :return:
    """

    folder_path = os.path.join(root_path, *parts)

    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)
        my_parts = list(parts) + [item]

        if item.startswith('.'):
            continue

        if os.path.isdir(path):
            upload_in_folder(root_path, *my_parts)
            continue

        key_name = '{}/{}'.format(key_prefix, '/'.join(my_parts))
        tracksim.log('[{}]: {}'.format(
            '/'.join(my_parts),
            key_name
        ))

        s3.upload_file(
            Filename=path,
            Bucket=bucket_name,
            Key=key_name,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': mimetypes.guess_type(item)[0]
            }
        )

upload_in_folder(tracksim.make_results_path('report'))
tracksim.log('[COMPLETE]: Trials have been deployed')
