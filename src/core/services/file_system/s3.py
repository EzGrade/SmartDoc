from dataclasses import dataclass
from typing import List

from .base import BaseFSProcessor
from ...repositories.aws.s3 import S3Repository


@dataclass
class S3FSProcessorConfig:
    """
    Configuration for S3FSProcessor.
    """

    s3_repository: S3Repository


class S3FSProcessor(BaseFSProcessor):
    """
    S3 file system processor.
    """

    errors = {
        "bucket_cannot_be_none": "Bucket name cannot be None",
    }
    s3_prefix = "s3://"

    def __init__(self, config: S3FSProcessorConfig):
        self._repository = config.s3_repository

    async def list(
        self,
        prefix: str,
        bucket: str | None,
    ) -> List[str]:
        """
        List files in the S3 bucket with the given prefix.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        return await self._repository.list_file(bucket, prefix)

    async def read(
        self,
        path: str,
        bucket: str | None,
    ) -> bytes:
        """
        Read a file from the S3 bucket.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        return await self._repository.get_file(bucket, path)

    async def read_batch(
        self,
        paths: List[str],
        bucket: str | None,
    ) -> List[bytes]:
        """
        Read multiple files from the S3 bucket.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        files = []
        for path in paths:
            files.append(await self.read(path=path, bucket=bucket))

        return files

    async def write(
        self,
        path: str,
        data: bytes,
        bucket: str | None,
        content_type: str | None = None,
    ) -> None:
        """
        Write a file to the S3 bucket.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        await self._repository.put_file(bucket, path, data, content_type=content_type)

    async def write_batch(
        self,
        data: List[tuple[str, bytes]],
        bucket: str | None,
    ) -> None:
        """
        Write multiple files to the S3 bucket.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        for pair in data:
            path, file = pair
            await self.write(path=path, data=file, bucket=bucket)

        return None

    async def delete(
        self,
        path: str,
        bucket: str | None,
    ) -> None:
        """
        Delete a file from the S3 bucket.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        await self._repository.delete_file(bucket, path)

    async def delete_batch(
        self,
        paths: List[str],
        bucket: str | None,
    ) -> None:
        """
        Delete multiple files from the S3 bucket.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        await self._repository.delete_files(bucket, paths)

    async def delete_files_by_prefix(
        self,
        prefix: str,
        bucket: str | None,
    ) -> None:
        """
        Delete all files in the S3 bucket with the given prefix.
        """
        if bucket is None:
            raise ValueError(self.errors["bucket_cannot_be_none"])

        await self._repository.delete_files_by_prefix(bucket, prefix)

    @classmethod
    def resolve_path(cls, path: str) -> tuple[str, str]:
        """
        Resolve the S3 path to bucket and path.
        """
        if not path.startswith(cls.s3_prefix):
            raise ValueError(f"Path must start with '{cls.s3_prefix}'")

        path = path.removeprefix(cls.s3_prefix)
        bucket, path = path.split("/", 1)
        return bucket, path

    @classmethod
    def path_to_local(cls, path: str) -> str:
        """
        Convert an S3 path to a local path.
        """
        if not path.startswith(cls.s3_prefix):
            raise ValueError(f"Path must start with '{cls.s3_prefix}'")

        path = path.removeprefix(cls.s3_prefix)
        return path
