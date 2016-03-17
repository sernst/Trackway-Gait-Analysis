import sys
import os
import mimetypes

import boto3
import tracksim
from tracksim import cli

DESCRIPTION = """
    Uploads existing trial and group data files to the AWS cloud, based on
    configuration settings specified in .tracksim.configs
    """

def execute_command():

    configs = cli.load_configs()
    aws = configs.get('aws')

    if not aws:
        cli.log('[ERROR]: No AWS configurations found in .tracksim.configs')
        sys.exit(1)

    profile = aws.get('profile')
    if not profile:
        boto3.setup_default_session(profile_name=configs.get('aws_profile'))

    bucket = aws.get('bucket')
    if not bucket:
        cli.log("""
            [ERROR]: No "bucket" specified in aws .tracksim.configs aws
            configuration
            """)
        sys.exit(1)

    key_prefix = aws.get('key_prefix')
    if not bucket:
        cli.log("""
            [ERROR]: No "key_prefix" specified in aws .tracksim.configs aws
            configuration
            """)
        sys.exit(1)

    upload_in_folder(aws, tracksim.make_results_path('report'))
    cli.log('[COMPLETE]: Trials have been deployed')

def upload_in_folder(aws_configs, root_path, *parts):
    """
    :param aws_configs:
    :param root_path:
    :param parts:
    :return:
    """

    s3 = boto3.client('s3')

    folder_path = os.path.join(root_path, *parts)

    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)
        my_parts = list(parts) + [item]

        if item.startswith('.'):
            continue

        if os.path.isdir(path):
            upload_in_folder(root_path, *my_parts)
            continue

        key_name = '{}/{}'.format(aws_configs['key_prefix'], '/'.join(my_parts))
        print('[{}]: {}'.format(
            '/'.join(my_parts),
            key_name
        ))

        s3.upload_file(
            Filename=path,
            Bucket=aws_configs['bucket'],
            Key=key_name,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': mimetypes.guess_type(item)[0]
            }
        )
