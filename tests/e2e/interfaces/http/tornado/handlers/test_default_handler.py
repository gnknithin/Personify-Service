from http import HTTPStatus

from infra.constants._string import (
    GenericConstants,
    HttpMethodConstants,
    MessagesConstants,
)
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
        assert hasattr(response, GenericConstants.ERROR)
        assert hasattr(response.error, GenericConstants.CODE)
        assert getattr(
            response.error, GenericConstants.CODE
        ) == HTTPStatus.NOT_FOUND
        assert hasattr(response.error, GenericConstants.MESSAGE)
        assert getattr(
            response.error, GenericConstants.MESSAGE
        ) == MessagesConstants.MSG_UNKNOWN_ENDPOINT


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
        assert hasattr(response,GenericConstants.ERROR)
        assert hasattr(response.error, GenericConstants.CODE)
        assert getattr(
            response.error, GenericConstants.CODE
        ) == HTTPStatus.NOT_FOUND
        assert hasattr(response.error, GenericConstants.MESSAGE)
        assert getattr(
            response.error, GenericConstants.MESSAGE
        ) == MessagesConstants.MSG_UNKNOWN_ENDPOINT