from logging import Logger
from typing import Optional

from infra.adapters.storage.base_storage_adapter import BaseStorageAdapter
from minio.api import Minio
from minio.lifecycleconfig import LifecycleConfig


class MinioAdapter(BaseStorageAdapter):
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

    def bucket_exists(self, name: str) -> bool:
        return self.client.bucket_exists(bucket_name=name)

    def create_bucket(self, name: str):
        return self.client.make_bucket(bucket_name=name)

    def get_bucket_lifecycle(self, name: str) -> Optional[LifecycleConfig]:
        return self.client.get_bucket_lifecycle(bucket_name=name)

    def get_bucket_policy(self, name: str):
        return self.client.get_bucket_policy(bucket_name=name)

    def list_buckets(self):
        return self.client.list_buckets()

    def delete_bucket(self, name: str):
        return self.client.remove_bucket(bucket_name=name)
