import logging
from http import HTTPStatus
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.factory.build_user_service import UserServiceFactory
from infra.constants._string import (
    GenericConstants,
    MessagesConstants,
)
from interfaces.http.tornado.handlers.base_handler import BaseRequestHandler
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema


class UserSignUpHandler(BaseRequestHandler):
    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any],
        service_factory: UserServiceFactory
    ) -> None:
        super().initialize(logger, schema_method_validators)
        self._user_service = service_factory.build(scope=self.request_id)

    async def post(self):
        """Creates a new user entry in user resource
        ---
        tags: [user]
        summary: Creates a new user entry in users resource
        description: Creates a new user entry in users resource
        requestBody:
            required: True
            content:
                application/json:
                    schema:
                        SignUpSchema
        responses:
            201:
                description: Created user successfully
                headers:
                    X-User-Id:
                        description: User ID
                        schema:
                            type: string
                            example: fhds98ew89y234hrfwou

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
        _result: Optional[UUID] = self._user_service.createUser(
            data=self.payload
        )
        if _result is not None:
            _status = HTTPStatus.CREATED
            self.set_header(GenericConstants.HEADER_USER_ID, str(_result))
        else:
            _errors: List[Any] = list()
            _errors.append(
                MessagesConstants.MSG_BAD_PARAMETER_INPUT_FORMAT
            )
            _errors.append(
                MessagesConstants.MSG_ACCOUNT_ALREADY_EXISTS
            )
            _response: Dict[Any, Any] = dict()
            _response[GenericConstants.SUCCESS] = False
            _response[GenericConstants.ERRORS] = _errors
            _data = BadRequestSchema().load(data=_response)
        # Return
        return self.build_response(status=_status, data=_data)
