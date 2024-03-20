from logging import Logger

from infra.adapters.storage.base_storage_adapter import BaseStorageAdapter
from minio.api import Minio


class MinIOAppUserAdapter(BaseStorageAdapter):
    def __init__(
        self,
        logger: Logger,
        host: str,
        access_key: str,
        secret_key: str,
        secure: bool,
    ) -> None:
        super().__init__(logger)
        self._client = Minio(
            endpoint=host, access_key=access_key, secret_key=secret_key, secure=secure
        )

    @property
    def client(self) -> Minio:
        return self._client

    def create_object(self, bucket_name: str, object_name: str, data: str):
        # https://min.io/docs/minio/linux/developers/python/API.html#put_object
        ...

    def delete_object(self, bucket_name: str, object_name: str):
        return self.client.remove_object(
            bucket_name=bucket_name, object_name=object_name, version_id=None
        )
