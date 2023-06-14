import logging
from http import HTTPStatus
from typing import Any, Dict, List, Optional

from app.factory.build_contact_service import ContactServiceFactory
from domain.contact_model import ContactModel
from infra.constants._string import GenericConstants, MessagesConstants
from interfaces.http.tornado.handlers.base_user_handler import BaseUserRequestHandler
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema
from interfaces.http.tornado.schemas.v1.contact_schema import (
    UserContactDetailSchema,
    UserContactSchema,
)


class ContactIdHandler(BaseUserRequestHandler):
    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any],
        service_factory: ContactServiceFactory
    ) -> None:
        super().initialize(
            logger, schema_method_validators, service_factory=service_factory
        )

    async def get(self, contact_id: str):
        """Retrieves Contact details
        ---
        tags: [Contact]
        summary: Find Contact By Id
        description: For valid ID, retrieves the contact details
        security:
            - bearerAuth: []
        parameters:
            - name: contact_id
              in: path
              description: The Contact Id of a User  
              required: true
              schema:
                type: string

        responses:
            200:
                description: Successfully returnes contact details
                content:
                    application/json:
                        schema:
                            UserContactDetailSchema
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
        _response: Dict[Any, Any] = dict()
        _result: Optional[ContactModel] = self._service.getUserContactById(
            user_id=self.user_id,
            contact_id=contact_id
        )
        if _result is not None:
            _status = HTTPStatus.OK
            _response[GenericConstants.SUCCESS] = True
            _response[GenericConstants.DATA] = UserContactSchema().dump(
                obj=_result)
            _data = UserContactDetailSchema().load(data=_response)
        else:
            _errors: List[Any] = list()
            _errors.append(
                MessagesConstants.MSG_BAD_PARAMETER_INPUT_FORMAT
            )
            _response[GenericConstants.SUCCESS] = False
            _response[GenericConstants.ERRORS] = _errors
            _data = BadRequestSchema().load(data=_response)
        # Return
        return self.build_response(status=_status, data=_data)
