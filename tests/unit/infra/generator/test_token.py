from typing import Any, Dict

from infra.generator.token import TokenGenerator

from tests.utils.base_tests import BaseUnitTest


class TestTokenGenerator(BaseUnitTest):

    def test_encode_and_return_successfully(self):
        # Arrange
        _data: Dict[Any, Any] = dict(hello="world")
        # Act
        sut = TokenGenerator.encode(
            data=_data
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, str)

    def test_decode_and_return_successfully(self):
        # Arrange
        _data: Dict[Any, Any] = dict(hello="world")
        _encoded = TokenGenerator.encode(
            data=_data
        )
        # Act
        sut = TokenGenerator.decode(value=_encoded)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert sut == _data
