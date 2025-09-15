from abc import ABC, abstractmethod
from typing import List


class BaseFSProcessor(ABC):
    """
    Base class for all file system processors.
    """

    @abstractmethod
    async def list(
        self,
        prefix: str,
        bucket: str | None,
    ) -> List[str]:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def read(
        self,
        path: str,
        bucket: str | None,
    ) -> bytes:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def read_batch(
        self,
        paths: List[str],
        bucket: str | None,
    ) -> List[bytes]:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def write(
        self,
        path: str,
        data: bytes,
        bucket: str | None,
        content_type: str | None = None,
    ) -> None:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def write_batch(
        self,
        data: List[tuple[str, bytes]],
        bucket: str | None,
    ) -> None:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def delete(
        self,
        path: str,
        bucket: str | None,
    ) -> None:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def delete_batch(
        self,
        paths: List[str],
        bucket: str | None,
    ) -> None:
        """
        Process the data and return the result.
        """
        pass

    @abstractmethod
    async def delete_files_by_prefix(
        self,
        prefix: str,
        bucket: str | None,
    ) -> None:
        """
        Process the data and return the result.
        """
        pass
