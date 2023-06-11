import logging
from http import HTTPStatus
from typing import Any, Dict, List, Union

from app.factory.build_user_service import UserServiceFactory
from app.user_service import UserService
from infra.constants._string import GenericConstants, MessagesConstants
from interfaces.http.tornado.handlers.base_handler import BaseRequestHandler
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema


class UserSignInHandler(BaseRequestHandler):
    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any],
        service_factory: UserServiceFactory
    ) -> None:
        super().initialize(logger, schema_method_validators)
        self._user_service: UserService = service_factory.build(
            scope=self.request_id)

    async def post(self):
        """Let user login using username and password
        ---
        tags: [User]
        summary: Sign In
        description: Logs user into the system
        requestBody:
            required: True
            content:
                application/json:
                    schema:
                        SignInSchema
        responses:
            200:
                description: successful operation
                headers:
                    Authorization:
                        description: Bearer toke
                        schema:
                            type: string
                            example: Bearer fhds98ew89y234hrfwou

            400:
                description: Invalid request format
                content:
                    application/json:
                        schema:
                            BadRequestSchema

            404:
                description: Invalid request content
                content:
                    application/json:
                        schema:
                            NotFoundSchema

            500:
                description: Server error
                content:
                    application/json:
                        schema:
                            ServerErrorSchema
        """
        _status: int = HTTPStatus.BAD_REQUEST
        _data: Any = None
        _result: Union[str, List[str]] = self._user_service.loginUserWithCredentials(
            self.payload)
        if isinstance(_result, str):
            _status = HTTPStatus.OK
            _bearer: str = f'{GenericConstants.BEARER} {_result}'
            self.set_header(
                name=GenericConstants.HEADER_AUTHORIZATION,
                value=_bearer
            )
        else:
            _errors: List[Any] = list()
            _errors.append(
                MessagesConstants.MSG_BAD_PARAMETER_INPUT_FORMAT
            )
            _errors.extend(_result)
            _response: Dict[Any, Any] = dict()
            _response[GenericConstants.SUCCESS] = False
            _response[GenericConstants.ERRORS] = _errors
            _data = BadRequestSchema().load(data=_response)
        # Return
        return self.build_response(status=_status, data=_data)
