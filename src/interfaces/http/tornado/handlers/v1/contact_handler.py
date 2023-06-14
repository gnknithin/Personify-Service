import logging
from http import HTTPStatus
from typing import Any, Dict, List, Optional

from app.factory.build_contact_service import ContactServiceFactory
from infra.constants._string import GenericConstants, MessagesConstants
from infra.constants._url import APIEndpointV1
from interfaces.http.tornado.handlers.base_user_handler import BaseUserRequestHandler
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema


class UserContactHandler(BaseUserRequestHandler):
    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any],
        service_factory: ContactServiceFactory
    ) -> None:
        super().initialize(
            logger, schema_method_validators, service_factory=service_factory
        )

    async def post(self):
        """Let user create a contact
        ---
        tags: [Contact]
        summary: Create Contact
        description: Create a Contact for an user
        requestBody:
            required: True
            description: Details required to create a contact
            content:
                application/json:
                    schema:
                        CreateContactSchema
        responses:
            201:
                description: Created User Contact Successfully
                headers:
                    location:
                        description: Contact details
                        schema:
                            type: string
                            example: '/api/v1/contact/{contact_id}'
                    X-Contact-Id:
                        description: Contact ID
                        schema:
                            type: string
                            example: fhdssfdgsghw89y234hrfwou
            400:
                description: Bad Request or Invalid request format
                content:
                    application/json:
                        schema:
                            BadRequestSchema

            404:
                description: Not Found or Invalid request content
                content:
                    application/json:
                        schema:
                            NotFoundSchema

            500:
                description: Internal Server Error
                content:
                    application/json:
                        schema:
                            ServerErrorSchema
        """
        _status: int = HTTPStatus.BAD_REQUEST
        _data: Any = None
        _result: Optional[str] = self._service.addUserContact(
            user_id=self.user_id,
            data=self.payload
        )
        if _result is not None:
            _status = HTTPStatus.CREATED
            _contact_id_uri = APIEndpointV1.CONTACT_BY_ID_URI.replace(
                '{contact_id}', _result)
            self.set_header(GenericConstants.HEADER_LOCATION, _contact_id_uri)
            self.set_header(GenericConstants.HEADER_CONTACT_ID, _result)
        else:
            _errors: List[Any] = list()
            _errors.append(
                MessagesConstants.MSG_BAD_PARAMETER_INPUT_FORMAT
            )
            _response: Dict[Any, Any] = dict()
            _response[GenericConstants.SUCCESS] = False
            _response[GenericConstants.ERRORS] = _errors
            _data = BadRequestSchema().load(data=_response)
        # Return
        return self.build_response(status=_status, data=_data)
