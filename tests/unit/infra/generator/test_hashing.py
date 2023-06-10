

from infra.generator.hashing import HashGenerator

from tests.utils.base_tests import BaseUnitTest


class TestHashGenerator(BaseUnitTest):

    def test_create_and_return_successfully(self):
        # Arrange
        _value = 'hello'
        _salt = 'world'
        # Act
        sut = HashGenerator.create(
            value=_value,
            salt=_salt
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, str)

    def test_is_valid_and_return_successfully(self):
        # Arrange
        _value = 'hello'
        _salt = 'world'
        _hashed_value: str = HashGenerator.create(
            value=_value,
            salt=_salt
        )
        # Act
        sut = HashGenerator.is_valid(
            hashed_value=_hashed_value,
            value=_value,
            salt=_salt
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        assert sut is True
