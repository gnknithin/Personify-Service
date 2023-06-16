from uuid import UUID

from infra.generator.identity import IdentityGenerator

from tests.utils.base_tests import BaseUnitTest


class TestIdentityGenerator(BaseUnitTest):

    def test_get_random_uuid4_and_return_successfuly(self):
        # Arrange
        # Act
        sut = IdentityGenerator.get_random_uuid4()
        # Assert
        assert sut is not None
        assert isinstance(sut, UUID)

    def test_get_random_id_and_return_successfuly(self):
        # Arrange
        # Act
        sut = IdentityGenerator.get_random_id()
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        assert len(sut) == 32

    def test_get_random_id_of_object_length_and_return_successfuly(self):
        # Arrange
        # Act
        sut = IdentityGenerator.get_random_id_of_object_length()
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        assert len(sut) == 24
