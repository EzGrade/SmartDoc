from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional

from loguru import logger

from shared.factories.aws.s3 import AwsClientFactory, AwsEnvConfig
from shared.helpers.aws.s3 import handle_s3_exceptions


class AsyncS3Client:
    """Async S3 client that handles authentication using AWS credentials"""

    def __init__(self, aws_env_config: AwsEnvConfig):
        self.aws_client_factory = AwsClientFactory(aws_env_config)

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator:
        async with self.aws_client_factory.get_s3_client() as client:
            yield client

    @handle_s3_exceptions
    async def upload_file(
            self,
            key: str,
            data: bytes,
            bucket: str,
            content_type: Optional[str] = None,
            metadata: Optional[Dict[str, str]] = None,
            extra_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Upload file to S3 bucket"""
        args = extra_args or {}
        if metadata:
            args["Metadata"] = metadata
        if content_type:
            args["ContentType"] = content_type

        async with self._get_client() as client:
            await client.put_object(Bucket=bucket, Key=key, Body=data, **args)
            logger.debug(f"Successfully uploaded file to s3://{bucket}/{key}")

    @handle_s3_exceptions
    async def download_file(self, bucket: str, key: str) -> bytes:
        """Download file from S3 bucket"""
        async with self._get_client() as client:
            response = await client.get_object(Bucket=bucket, Key=key)
            async with response["Body"] as stream:
                data = await stream.read()
                logger.debug(f"Successfully downloaded file from s3://{bucket}/{key}")
                return data

    @handle_s3_exceptions
    async def list_objects(
            self, bucket: str, prefix: str, max_keys: int = 1000
    ) -> Dict:
        """List objects in S3 bucket with prefix"""
        async with self._get_client() as client:
            response = await client.list_objects_v2(
                Bucket=bucket, Prefix=prefix, MaxKeys=max_keys
            )
            logger.debug(
                f"Successfully listed objects with prefix '{prefix}' in bucket '{bucket}'"
            )
            return response

    @handle_s3_exceptions
    async def delete_object(self, key: str, bucket: str) -> None:
        """Delete an object from S3 bucket"""
        async with self._get_client() as client:
            await client.delete_object(Bucket=bucket, Key=key)
            logger.debug(f"Successfully deleted s3://{bucket}/{key}")

    @handle_s3_exceptions
    async def delete_objects(self, keys: list[str], bucket: str) -> None:
        """Delete multiple objects from S3 bucket"""
        async with self._get_client() as client:
            objects = [{"Key": key} for key in keys]
            await client.delete_objects(Bucket=bucket, Delete={"Objects": objects})
            logger.debug(f"Successfully deleted objects from s3://{bucket}")
