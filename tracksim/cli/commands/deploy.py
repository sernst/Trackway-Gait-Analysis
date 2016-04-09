import sys
import os
import mimetypes
from argparse import ArgumentParser

import boto3
import tracksim
from tracksim import cli

DESCRIPTION = """
    Uploads existing trial and group data files to the AWS cloud
    """

def get_aws_settings(
        configs: dict,
        bucket: str = None,
        profile: str = None,
        root_path: str = None
) -> str:
    """
    Returns a dictionary containing the AWS configuration settings for
    uploading report files to and Amazon Web Services S3 bucket

    :param configs:
        Command line configuration settings
    :param bucket:
        The name of the bucket where the files will be uploaded. If none is
        provided, the bucket name will be loaded from the configs
    :param profile:
        The name of the profile to use to access the AWS credentials. If none is
        provided, the profile name will be loaded from the configs
    :param root_path:
        The root folder in the S3 bucket where the files will be uploaded. If
        none is provided, the root will be loaded from the configs
    """

    def error_and_exit(label, key):
        tracksim.log("""
            [ERROR]: No {label} was specified in your tracksim settings.

            Use the configure command to fix this:

                $ tracksim configure {key} "[{LABEL}]"

            or specify the {label} in your deploy command. For details run:

                $ tracksim deploy help
            """.format(label=label, key=key, LABEL=label.upper()))
        sys.exit(1)

    out = dict()

    entries = [
        (profile, 'aws.profile', 'profile'),
        (bucket, 'aws.bucket', 'bucket'),
        (root_path, 'aws.root_path', 'root_path')
    ]

    for e in entries:
        value = e[0]
        if not value:
            value = configs.get(e[1])
        if not value:
            error_and_exit(label=e[2], key=e[1])
        out[e[2]] = value

    return out

def execute_command():
    """ Runs the deploy command """

    parser = ArgumentParser()

    parser.description = cli.reformat(DESCRIPTION)

    parser.add_argument(
        'deploy',
        type=str,
        help='The deploy command to execute'
    )

    parser.add_argument(
        'root_path',
        type=str,
        help=cli.reformat("""
            The folder in the S3 bucket where your files will be uploaded
            """)
    )

    parser.add_argument(
        '-p', '--profile',
        dest='profile',
        type=str,
        default=None,
        help=cli.reformat("""
            The name of the AWS credentials profile to use for access to the
            AWS S3 bucket resources
            """)
    )

    parser.add_argument(
        '-b', '--bucket',
        dest='bucket',
        type=str,
        default=None,
        help=cli.reformat("""
            The name of the S3 bucket where the files will be uploaded
            """)
    )

    args = vars(parser.parse_args())
    configs = cli.load_configs()

    upload_in_folder(
        get_aws_settings(configs, **args),
        tracksim.make_results_path('report')
    )
    tracksim.log('[COMPLETE]: Trials have been deployed')

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

        key_name = '{}/{}'.format(
            aws_configs['root_path'].strip('/'),
            '/'.join(my_parts)
        )

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
