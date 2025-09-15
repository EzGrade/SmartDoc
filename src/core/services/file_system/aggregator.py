from dataclasses import dataclass
from typing import List

from loguru import logger

from configs.file_system import FileSystemConfig
from shared.enums.services.core.file_system import FSProvidersEnum
from .base import BaseFSProcessor
from .local import LocalFSProcessor
from .s3 import S3FSProcessor


@dataclass
class FSAggregatorConfig:
    local_fs_processor: LocalFSProcessor
    s3_fs_processor: S3FSProcessor

    fs_config: FileSystemConfig


class FSAggregator:
    def __init__(self, config: FSAggregatorConfig):
        self._local_fs_processor = config.local_fs_processor
        self._s3_fs_processor = config.s3_fs_processor
        self._fs_config = config.fs_config

    @property
    def fs_config(self) -> FileSystemConfig:
        return self._fs_config

    def __get_fs_processor(
            self,
            provider: FSProvidersEnum,
    ) -> BaseFSProcessor:
        match provider:
            case FSProvidersEnum.LOCAL:
                return self._local_fs_processor
            case FSProvidersEnum.S3 if self._fs_config.USE_AWS_S3:
                return self._s3_fs_processor
            case _:
                logger.warning(
                    f"Provider {provider} is disabled. Using local file system."
                )
                self._local_fs_processor.target_provider = provider
                return self._local_fs_processor

    @classmethod
    def parse_s3_path(cls, s3_path: str) -> tuple[str, str]:
        return S3FSProcessor.resolve_path(s3_path)

    async def list(
            self,
            provider: FSProvidersEnum,
            prefix: str,
            bucket: str | None = None,
    ) -> list[str]:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.list(
            prefix=prefix,
            bucket=bucket,
        )

    async def read(
            self,
            provider: FSProvidersEnum,
            path: str,
            bucket: str | None = None,
    ) -> bytes:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.read(
            path=path,
            bucket=bucket,
        )

    async def read_batch(
            self,
            provider: FSProvidersEnum,
            paths: List[str],
            bucket: str | None = None,
    ) -> List[bytes]:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.read_batch(
            paths=paths,
            bucket=bucket,
        )

    async def write(
            self,
            provider: FSProvidersEnum,
            path: str,
            data: bytes,
            bucket: str | None = None,
            content_type: str | None = None,
    ) -> None:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.write(
            path=path,
            data=data,
            bucket=bucket,
            content_type=content_type,
        )

    async def write_batch(
            self,
            provider: FSProvidersEnum,
            data: List[tuple[str, bytes]],
            bucket: str | None = None,
    ) -> None:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.write_batch(
            data=data,
            bucket=bucket,
        )

    async def delete(
            self,
            provider: FSProvidersEnum,
            path: str,
            bucket: str | None = None,
    ) -> None:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.delete(
            path=path,
            bucket=bucket,
        )

    async def delete_batch(
            self,
            provider: FSProvidersEnum,
            paths: List[str],
            bucket: str | None = None,
    ) -> None:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.delete_batch(
            paths=paths,
            bucket=bucket,
        )

    async def delete_files_by_prefix(
            self,
            provider: FSProvidersEnum,
            prefix: str,
            bucket: str | None = None,
    ) -> None:
        fs_processor = self.__get_fs_processor(provider)
        return await fs_processor.delete_files_by_prefix(
            prefix=prefix,
            bucket=bucket,
        )
