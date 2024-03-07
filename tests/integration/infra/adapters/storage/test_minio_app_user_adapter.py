from tests.utils.base_tests import BaseIntegrationTest


class TestMinIOAppUserAdapter(BaseIntegrationTest):
    # def test_should_delete_bucket_and_raise_s3error(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     # Act
    #     with pytest.raises(S3Error) as exec_info:
    #         _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #         assert exec_info.type is S3Error

    # def test_should_delete_bucket_and_return_successfully(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     _create_bucket = _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #     assert _create_bucket is None
    #     # Act
    #     sut = _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #     # Assert
    #     assert sut is None

    # def test_should_create_bucket_and_return_successfully(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     # Act
    #     sut = _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #     # Assert
    #     assert sut is None
    #     # Cleanup
    #     _delete_bucket = _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #     assert _delete_bucket is None

    # def test_should_create_existing_bucket_and_raise_s3error(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     _create_bucket = _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #     assert _create_bucket is None
    #     # Act
    #     with pytest.raises(S3Error) as exec_info:
    #         _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #         assert exec_info.type is S3Error
    #     # Cleanup
    #     _delete_bucket = _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #     assert _delete_bucket is None

    # def test_should_check_bucket_exists_return_false(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     # Act
    #     sut = _minio_app_user_adapter.bucket_exists(bucket_name=_random_name)
    #     # Assert
    #     assert sut is False

    # def test_should_check_bucket_exists_return_true(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     _create_bucket = _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #     assert _create_bucket is None
    #     # Act
    #     sut = _minio_app_user_adapter.bucket_exists(bucket_name=_random_name)
    #     # Assert
    #     assert sut is True
    #     # Cleanup
    #     _delete_bucket = _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #     assert _delete_bucket is None

    # def test_should_get_bucket_policy_and_return_successfully(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     _create_bucket = _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #     assert _create_bucket is None
    #     # Act
    #     with pytest.raises(S3Error) as exec_info:
    #         _ = _minio_app_user_adapter.get_bucket_policy(bucket_name=_random_name)
    #         assert exec_info.type is S3Error
    #     # Cleanup
    #     _delete_bucket = _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #     assert _delete_bucket is None

    # def test_should_get_bucket_lifecycle_and_return_successfully(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _random_name = f"{IdentityGenerator().get_random_id()}"
    #     _create_bucket = _minio_app_user_adapter.create_bucket(bucket_name=_random_name)
    #     assert _create_bucket is None
    #     # Act
    #     sut = _minio_app_user_adapter.get_bucket_lifecycle(bucket_name=_random_name)
    #     # Assert
    #     assert sut is None
    #     # Cleanup
    #     _delete_bucket = _minio_app_user_adapter.delete_bucket(bucket_name=_random_name)
    #     assert _delete_bucket is None

    # def test_should_list_buckets_and_return_empty_successfully(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     # Act
    #     sut = _minio_app_user_adapter.list_buckets()
    #     # Assert
    #     assert sut is not None
    #     assert isinstance(sut, list)
    #     assert len(sut) == 0

    # def test_should_list_buckets_and_return_few_successfully(
    #     self, init_bootstrap: ApplicationBootstrap
    # ):
    #     # Arrange
    #     _minio_app_user_adapter = init_bootstrap.minio_app_user_adapter
    #     _bucket_ids: List[str] = list()
    #     for _ in range(10):
    #         _random_name = f"{IdentityGenerator().get_random_id()}"
    #         _create_bucket = _minio_app_user_adapter.create_bucket(
    #             bucket_name=_random_name
    #         )
    #         assert _create_bucket is None
    #         _bucket_ids.append(_random_name)

    #     # Act
    #     sut = _minio_app_user_adapter.list_buckets()
    #     # Assert
    #     assert sut is not None
    #     assert isinstance(sut, list)
    #     assert len(sut) == 10
    #     for _each in sut:
    #         assert _each is not None
    #         assert isinstance(_each, Bucket)

    #     # Cleanup
    #     for _each in _bucket_ids:
    #         _delete_bucket = _minio_app_user_adapter.delete_bucket(bucket_name=_each)
    #         assert _delete_bucket is None
    #     # Act
    #     sut = _minio_app_user_adapter.list_buckets()
    #     # Assert
    #     assert sut is not None
    #     assert isinstance(sut, list)
    #     assert len(sut) == 0
    ...
