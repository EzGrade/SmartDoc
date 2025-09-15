from configs.aws.s3 import AwsEnvConfig
from core.repositories.aws.s3 import S3Repository


def get_s3_repository():
    config = AwsEnvConfig()
    return S3Repository(aws_env_config=config)
