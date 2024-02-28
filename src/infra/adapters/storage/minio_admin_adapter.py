from json import loads
from logging import Logger
from typing import Any, Dict

from infra.adapters.storage.base_storage_adapter import BaseStorageAdapter
from minio.credentials.providers import AssumeRoleProvider
from minio.minioadmin import MinioAdmin


class MinIOAdminAdapter(BaseStorageAdapter):
    def __init__(
        self,
        logger: Logger,
        host: str,
        access_key: str,
        secret_key: str,
        secure: bool,
    ) -> None:
        super().__init__(logger)
        _sts_endpoint: str = f"https://{host}" if secure else f"http://{host}"
        _provider = AssumeRoleProvider(
            sts_endpoint=_sts_endpoint, access_key=access_key, secret_key=secret_key
        )
        self._admin = MinioAdmin(
            endpoint=host,
            credentials=_provider,
            secure=secure,
            cert_check=False,
        )

    @property
    def admin(self) -> MinioAdmin:
        return self._admin

    def info(self) -> Dict[Any, Any]:

        return loads(self._admin.info())

    def check_avilability(self) -> bool:
        _result: bool = False
        _response = self.info()
        if "mode" in _response:
            if _response["mode"] == "online":
                _result = True
        return _result
