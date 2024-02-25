from logging import Logger
from typing import List, Optional

from infra.adapters.storage.base_storage_adapter import BaseStorageAdapter
from minio.api import Minio
from minio.datatypes import Bucket
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
        # TODO DEBUG Credentials
        self._logger.info(msg=f"Host = {host}")
        self._logger.info(msg=f"Access Key = {access_key}")
        self._logger.info(msg=f"Secret Key = {secret_key}")
        self._logger.info(msg=f"Secure = {secure}")
        self._logger.info(msg=f"Secure Type = {type(secure)}")
        self._client = Minio(
            endpoint=host, access_key=access_key, secret_key=secret_key, secure=secure
        )

    @property
    def client(self) -> Minio:
        return self._client

    def bucket_exists(self, bucket_name: str) -> bool:
        return self.client.bucket_exists(bucket_name=bucket_name)

    def create_bucket(self, bucket_name: str) -> None:
        return self.client.make_bucket(bucket_name=bucket_name)

    def get_bucket_lifecycle(self, bucket_name: str) -> Optional[LifecycleConfig]:
        return self.client.get_bucket_lifecycle(bucket_name=bucket_name)

    def get_bucket_policy(self, bucket_name: str) -> str:
        return self.client.get_bucket_policy(bucket_name=bucket_name)

    def list_buckets(self) -> List[Bucket]:
        return self.client.list_buckets()

    def delete_bucket(self, bucket_name: str) -> None:
        return self.client.remove_bucket(bucket_name=bucket_name)

    # def create_object(self, bucket_name: str, object_name: str, data: str):
    #     return self.client.put_object()
