from api.v1.dependencies.core.repositories.aws.s3 import get_s3_repository
from configs.file_system import FileSystemConfig
from core.services.file_system.aggregator import FSAggregator, FSAggregatorConfig
from core.services.file_system.local import LocalFSProcessor
from core.services.file_system.s3 import S3FSProcessor, S3FSProcessorConfig


def get_s3_file_system_config() -> S3FSProcessorConfig:
    return S3FSProcessorConfig(s3_repository=get_s3_repository())


def get_file_system_aggregator_config() -> FSAggregatorConfig:
    config = FileSystemConfig()

    local_file_system = LocalFSProcessor()
    s3_file_system = S3FSProcessor(config=get_s3_file_system_config())
    return FSAggregatorConfig(
        fs_config=config,
        local_fs_processor=local_file_system,
        s3_fs_processor=s3_file_system,
    )


def get_file_system_aggregator() -> FSAggregator:
    return FSAggregator(
        config=get_file_system_aggregator_config()
    )
