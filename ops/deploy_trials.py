import os
import json
import mimetypes

import boto3
import tracksim

CONFIGS_PATH = tracksim.make_project_path('ops', 'configs.json')

if not os.path.exists(CONFIGS_PATH):
    raise FileNotFoundError('Missing configs.json file')

with open(CONFIGS_PATH, 'r') as f:
    configs = json.load(f)

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

        print('[UPLOADING]:', '/'.join(my_parts))

        s3.upload_file(
            Filename=path,
            Bucket=bucket_name,
            Key='{}/{}'.format(key_prefix, '/'.join(parts)),
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': mimetypes.guess_type(item)[0]
            }
        )

upload_in_folder(tracksim.make_results_path('report'))
print('[COMPLETE]: Trials have been deployed')
