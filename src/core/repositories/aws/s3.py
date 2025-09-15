from core.clients.aws.s3 import AsyncS3Client


class S3Repository(AsyncS3Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def get_file(self, bucket: str, path: str) -> bytes:
        return await self.download_file(
            bucket=bucket,
            key=path,
        )

    async def list_file(self, bucket: str, prefix: str) -> list:
        response = await self.list_objects(
            bucket=bucket,
            prefix=prefix,
        )
        return [
            obj["Key"] for obj in response.get("Contents", []) if obj["Key"] != prefix
        ]

    async def put_file(
            self, bucket: str, path: str, data: bytes, content_type: str | None = None
    ) -> None:
        await self.upload_file(
            bucket=bucket,
            key=path,
            data=data,
            content_type=content_type,
        )

    async def delete_file(self, bucket: str, path: str) -> None:
        await self.delete_object(
            bucket=bucket,
            key=path,
        )

    async def delete_files(self, bucket: str, keys: list[str]) -> None:
        await self.delete_objects(
            bucket=bucket,
            keys=keys,
        )

    async def delete_files_by_prefix(self, bucket: str, prefix: str) -> None:
        objects = await self.list_objects(
            bucket=bucket,
            prefix=prefix,
        )
        keys = [obj["Key"] for obj in objects.get("Contents", [])]
        if keys:
            await self.delete_objects(
                bucket=bucket,
                keys=keys,
            )
        else:
            raise ValueError(
                f"No objects found with prefix '{prefix}' in bucket '{bucket}'"
            )
