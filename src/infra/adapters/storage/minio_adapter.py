from logging import Logger
from typing import Type

from minio import Minio

from .base_storage_adapter import BaseStorageAdapter


class MinioAdapter(BaseStorageAdapter):
    def __init__(
        self, logger: Logger, host: str, access_key: str, secret_key: str
    ) -> None:
        super().__init__(logger)
        self._client: Type[Minio] = Minio(
            endpoint=host,
            access_key=access_key,
            secret_key=secret_key
        )

    def check_availability(self) -> bool:
        """
        Check availability

        # Return

        bool
        """
        raise NotImplementedError
