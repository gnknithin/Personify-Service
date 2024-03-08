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

    def server_info(self) -> Dict[Any, Any]:
        return loads(self._admin.info())

    def check_avilability(self) -> bool:
        _result: bool = False
        _response = self.server_info()
        if "mode" in _response:
            if _response["mode"] == "online":
                _result = True
        return _result

    def add_user(self, user_access_key: str, user_secret_key: str) -> str:
        return self.admin.user_add(
            access_key=user_access_key, secret_key=user_secret_key
        )

    def get_user_info(self, user_access_key: str) -> Dict[Any, Any]:
        return loads(self.admin.user_info(access_key=user_access_key))

    def enable_user(self, user_access_key: str):
        return self.admin.user_enable(access_key=user_access_key)

    def disable_user(self, user_access_key: str):
        return self.admin.user_disable(access_key=user_access_key)

    def is_user_enabled(self, user_access_key: str) -> bool:
        _result = False
        _response = self.get_user_info(user_access_key=user_access_key)
        if "status" in _response:
            if _response["status"] == "enabled":
                _result = True
        return _result

    def get_users(self) -> Dict[Any, Any]:
        return loads(self.admin.user_list())

    def check_user_exists(self, user_access_key: str) -> bool:
        _result: bool = False
        _response = self.get_users()
        if user_access_key in _response:
            _result = True
        return _result

    def delete_user(self, user_access_key: str) -> str:
        return self.admin.user_remove(access_key=user_access_key)
