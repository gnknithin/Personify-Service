from http import HTTPStatus

from infra.constants._string import HttpMethodConstants, MessagesConstants
from infra.constants._url import HandlerConstants

from tests.utils.base_tests import MainApplicationTestSetup


class TestDefaultHandler(MainApplicationTestSetup):

    def test_should_evaluate_default_handler_from_unknown_path_properly(self):
        _path = '/unknow-path'
        # Arrange, Act
        response = self.fetch(
            path=_path,
            method=HttpMethodConstants.GET,
            headers=None,
        )

        # Assert
        assert response.code == HTTPStatus.NOT_FOUND
        assert response.error.code == HTTPStatus.NOT_FOUND
        assert response.error.message == MessagesConstants.MSG_UNKNOWN_ENDPOINT


    def test_should_evaluate_default_handler_from_root_path_properly(self):
        _path = HandlerConstants.ROOT
        # Arrange, Act
        response = self.fetch(
            path=_path,
            method=HttpMethodConstants.GET,
            headers=None,
        )

        # Assert
        assert response.code == HTTPStatus.NOT_FOUND
        assert response.error.code == HTTPStatus.NOT_FOUND
        assert response.error.message == MessagesConstants.MSG_UNKNOWN_ENDPOINT