import os

import pytest
from bootstrap import ApplicationBootstrap
from infra.constants._string import MinioConstants
from infra.generator.identity import IdentityGenerator
from minio.error import S3Error

from tests.utils.base_tests import BaseIntegrationTest


class TestMinIOAppUserAdapter(BaseIntegrationTest):
    def test_should_delete_random_bucket_from_random_object_and_raise_S3Error(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_app_user = init_bootstrap.minio_app_user_adapter
        _random_bucket_name = f"{IdentityGenerator().get_random_id()}"
        _random_object_name = f"{IdentityGenerator().get_random_id()}"
        # Act
        with pytest.raises(S3Error) as exec_info:
            _ = _minio_app_user.delete_object(
                bucket_name=_random_bucket_name, object_name=_random_object_name
            )
            assert exec_info.type is S3Error

    def test_should_delete_random_object_from_existing_bucket_and_raise_S3Error(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_app_user = init_bootstrap.minio_app_user_adapter

        _existing_bucket_name = os.environ.get(
            MinioConstants.ENVVAR_MINIO_BUCKET_NAME, None
        )
        assert _existing_bucket_name is not None
        _random_object_name = f"{IdentityGenerator().get_random_id()}"
        # Act
        with pytest.raises(S3Error) as exec_info:
            _ = _minio_app_user.delete_object(
                bucket_name=_existing_bucket_name, object_name=_random_object_name
            )
            assert exec_info.type is S3Error
