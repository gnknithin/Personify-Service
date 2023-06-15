import logging
from http import HTTPStatus
from typing import Any, Dict, List, Optional

from app.factory.build_contact_service import ContactServiceFactory
from domain.contact_model import ContactModel
from infra.constants._string import (
    GenericConstants,
    HandlerQueryConstants,
    MessagesConstants,
)
from infra.constants._url import APIEndpointV1
from infra.validators.query_argument.base_query_validator import (
    BaseQueryArgumentValidator,
)
from infra.validators.query_argument.handler_query_argument_validator import (
    HandlerQueryArgumentValidator,
)
from interfaces.http.tornado.handlers.base_user_handler import (
    BaseUserQueryableRequestHandler,
)
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema
from interfaces.http.tornado.schemas.v1.contact_schema import (
    UserContactSchema,
    UserContactsListSchema,
)


class ContactHandler(BaseUserQueryableRequestHandler):
    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any],
        service_factory: ContactServiceFactory,
        query_argument_validator: Optional[
            BaseQueryArgumentValidator
        ] = HandlerQueryArgumentValidator
    ) -> None:
        super().initialize(
            logger,
            schema_method_validators,
            service_factory=service_factory,
            query_argument_validator=query_argument_validator
        )

    def _process_query_arguments(self) -> Dict[Any, Any]:
        _query_args: Dict[Any, Any] = dict()

        _query_args[
            HandlerQueryConstants.OFFSET
        ] = self.get_query_argument(
            HandlerQueryConstants.OFFSET, "0"
        )

        _query_args[
            HandlerQueryConstants.LIMIT
        ] = self.get_query_argument(HandlerQueryConstants.LIMIT, "5")

        return self.query_argument_validator.validate(**_query_args)

    async def get(self):
        """List all the user contacts based on parameter
        ---
        tags: [Contact]
        summary: List Contacts
        description: List all the user contacts based on parameter
        security:
            - bearerAuth: []
        parameters:
            - name: offset
              in: query
              description: Specifies the page number of the shifts to be displayed
              required: false
              schema:
                type: integer
              example: '0'
            - name: limit
              in: query
              description: Limits the number of items on a page
              required: false
              schema:
                type: integer
              example: '5'
        responses:
            200:
                description: Successfully returned shift eligibility details
                content:
                    application/json:
                        schema:
                            UserContactsListSchema
            204:
                description: No Content
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
        _status: int = HTTPStatus.OK
        _data: Any = None
        _result: List[ContactModel] = self._service.getUserContacts(
            user_id=self.user_id,
            **self.validated_query_args
        )
        if len(_result) == 0:
            _status = HTTPStatus.NO_CONTENT
        else:
            _contacts: Any = UserContactSchema(many=True).dump(obj=_result)

            _response: Dict[Any, Any] = dict()
            _response[GenericConstants.SUCCESS] = True
            _response[GenericConstants.DATA] = _contacts

            _data = UserContactsListSchema().load(data=_response)
        # Return
        return self.build_response(status=_status, data=_data)

    async def post(self):
        """Let user create a contact
        ---
        tags: [Contact]
        summary: Create Contact
        description: Create a Contact for an user
        security:
            - bearerAuth: []
        requestBody:
            required: True
            description: Details required to create a contact
            content:
                application/json:
                    schema:
                        ContactSchema
        responses:
            201:
                description: Created User Contact Successfully
                headers:
                    location:
                        description: URL to get the created contact
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
