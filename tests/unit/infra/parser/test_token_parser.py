from infra.parser.token_parser import AuthenticationBearerTokenParser

from tests.utils.base_tests import BaseUnitTest


class TestAuthenticationBearerTokenParser(BaseUnitTest):

    def test_should_return_invalid_token(self):
        # Arrange
        # Act
        sut = AuthenticationBearerTokenParser.extract(
            value="Bear Says-Hello"
        )
        # Assert
        assert sut is None

    def test_should_return_valid_token(self):
        # Arrange
        # Act
        sut = AuthenticationBearerTokenParser.extract(
            value="Bearer Says-Hello-Authentication"
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, str)

    def test_should_return_another_valid_token(self):
        # Arrange
        # Act
        sut = AuthenticationBearerTokenParser.extract(
            value="Bearer aflgahfjghafldjkghalkfdhglafdgafhgiafdgk"
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
