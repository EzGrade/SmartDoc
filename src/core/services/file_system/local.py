import asyncio
import os
from typing import List

from loguru import logger
import aiofiles

from configs.file_system import FileSystemConfig
from shared.enums.services.core.file_system import FSProvidersEnum
from .base import BaseFSProcessor


class LocalFSProcessor(BaseFSProcessor):
    """
    LocalFSProcessor is a class that handles file system operations for local files.
    It inherits from the BaseFSProcessor class.
    """

    def __init__(self):
        self.__fs_config = FileSystemConfig()
        self.__local_s3_path = self.__get_local_path(
            path=self.__fs_config.LOCAL_AWS_S3_PATH
        )

        self.target_provider: FSProvidersEnum = FSProvidersEnum.LOCAL

    @staticmethod
    def __get_local_path(
            path: str,
    ) -> str:
        pwd = os.getcwd()
        local_path = os.path.join(pwd, path)
        os.makedirs(local_path, exist_ok=True)
        return local_path

    def __get_full_path(self, path: str) -> str:
        """
        Get the full path to the local S3 folder.
        """
        match self.target_provider:
            case FSProvidersEnum.LOCAL:
                return path
            case FSProvidersEnum.S3:
                return os.path.join(self.__local_s3_path, path)
            case _:
                raise ValueError(f"Provider {self.target_provider} is not supported.")

    async def list(self, prefix: str, bucket: str | None = None) -> List[str]:
        """
        Get a list of files in the folder.
        """
        prefix = self.__get_full_path(prefix)
        return await asyncio.to_thread(
            lambda: [
                os.path.join(prefix, file)
                for file in os.listdir(prefix)
                if os.path.isfile(os.path.join(prefix, file))
            ]
        )

    async def read(self, path: str, bucket: str | None = None) -> bytes:
        """
        Process the data and return the result.
        """
        async with aiofiles.open(self.__get_full_path(path), mode="rb") as f:
            return await f.read()

    async def read_batch(
            self, paths: List[str], bucket: str | None = None
    ) -> List[bytes]:
        """
        Process the data and return the result.
        """
        files: list[bytes] = []
        for path in paths:
            files.append(await self.read(path))

        return files

    async def write(
            self,
            path: str,
            data: bytes,
            bucket: str | None = None,
            content_type: str | None = None,
    ) -> None:
        """
        Process the data and return the result.
        """
        logger.warning(f"Writing file {path} to local storage.")
        full_path = self.__get_full_path(path)
        dir_name = os.path.dirname(full_path)
        os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
        async with aiofiles.open(full_path, mode="wb") as f:
            await f.write(data)

    async def write_batch(
            self, data: List[tuple[str, bytes]], bucket: str | None = None
    ) -> None:
        """
        Process the data and return the result.
        """
        for path, file in data:
            await self.write(path, file)

    async def delete(self, path: str, bucket: str | None = None) -> None:
        """
        Process the data and return the result.
        """
        path = self.__get_full_path(path)
        if os.path.exists(path):
            await asyncio.to_thread(os.remove, path)
        else:
            raise FileNotFoundError(f"File {path} not found.")

    async def delete_batch(self, paths: List[str], bucket: str | None = None) -> None:
        """
        Process the data and return the result.
        """
        for path in paths:
            await self.delete(path)

    async def delete_files_by_prefix(
            self, prefix: str, bucket: str | None = None
    ) -> None:
        """
        Process the data and return the result.
        """
        files = await self.list(prefix)
        for file in files:
            await self.delete(file)
