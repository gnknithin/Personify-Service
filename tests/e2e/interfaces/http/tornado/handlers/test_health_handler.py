import json
from http import HTTPStatus

from infra.constants._string import GenericConstants, HttpMethodConstants
from infra.constants._url import HandlerConstants

from tests.utils.base_tests import MainApplicationTestSetup


class TestHealthHandler(MainApplicationTestSetup):

    def test_should_check_health_handler_properly(self):
        # Arrange
        # Act
        response = self.fetch(
            path=HandlerConstants.HEALTH_URI,
            method=HttpMethodConstants.GET,
            headers=self._get_headers()
        )
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        # Assert
        assert response.code == HTTPStatus.OK
        assert len(decoded_body) == 1
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is True
