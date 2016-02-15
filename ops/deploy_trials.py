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

directory = tracksim.make_results_path('report')
for item in os.listdir(directory):
    path = os.path.join(directory, item)
    if os.path.isdir(path) or item.startswith('.'):
        continue

    print('[UPLOADING]:', path)
    s3.upload_file(
        Filename=path,
        Bucket=bucket_name,
        Key='{}/{}'.format(key_prefix, item),
        ExtraArgs={
            'ACL': 'public-read',
            'ContentType': mimetypes.guess_type(item)[0]
        }
    )

directory = tracksim.make_results_path('report', 'trials')
for item in os.listdir(directory):
    path = os.path.join(directory, item)
    if os.path.isdir(path):
        continue

    print('[UPLOADING]:', path)
    s3.upload_file(
        Filename=path,
        Bucket=bucket_name,
        Key='{}/trials/{}'.format(key_prefix, item),
        ExtraArgs={
            'ACL': 'public-read',
            'ContentType': mimetypes.guess_type(item)[0]
        }
    )

print('[COMPLETE]: Trials have been deployed')
