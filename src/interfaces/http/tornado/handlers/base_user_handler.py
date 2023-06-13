import json
import logging
from http import HTTPStatus
from typing import Any, Awaitable, Dict, List, Optional
from uuid import UUID

import jwt
from app.factory.build_base_service import BaseServiceFactory
from infra.constants._string import (
    FieldNameConstants,
    GenericConstants,
    HttpConstants,
    MessagesConstants,
)
from infra.generator.identity import IdentityGenerator
from infra.generator.token import TokenGenerator
from infra.logging.logger import Logger
from infra.parser.token_parser import AuthenticationBearerTokenParser
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema
from tornado.escape import json_decode
from tornado.web import HTTPError, RequestHandler


class BaseUserRequestHandler(RequestHandler):

    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any],
        service_factory: BaseServiceFactory
    ) -> None:
        self.logger = logger
        self.schema_method_validators = schema_method_validators
        self.request_id: str = IdentityGenerator.get_random_id()
        self.payload: Any = None
        self._service: Any = service_factory.build(
            scope=self.request_id)

    def prepare(self) -> Optional[Awaitable[None]]:
        self._set_log_context()
        self._set_authentication_context()
        self._parse_json_body()
        return super().prepare()

    def _parse_json_body(self) -> None:
        if self.request.method not in HttpConstants.WRITE_OPERATIONS:
            return

        if (
            self.request.headers[
                HttpConstants.HEADER_CONTENT_TYPE
            ] == HttpConstants.MIME_TYPE_JSON
        ):
            schema = self.__get_method_schema()

            received_body = self._validate_json_body(self.request.body)

            validation_errors = schema().validate(received_body)

            if validation_errors:
                errors: List[Any] = list()
                if isinstance(received_body, json.JSONDecodeError):
                    errors.append(str(received_body))

                errors.extend(
                    [f'{k}: {v}' for k, v in validation_errors.items()]
                )

                return self._raise_invalid_request(msg=errors)

            self.payload = schema().load(received_body)

    def __get_method_schema(self):
        selected_schema = self.schema_method_validators.get(
            self.request.method
        )

        if selected_schema is None:
            _msg = f'Schema validator wasn\'t found for method: {self.request.method}'
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                log_message=_msg
            )
        return selected_schema

    def _raise_invalid_request(
        self, msg: Optional[List[Any]] = None
    ):
        errors: List[Any] = list()
        errors.append(MessagesConstants.MSG_INVALID_SCHEMA_VALIDATION)
        if msg is not None:
            errors.extend(msg)

        self.build_response(
            HTTPStatus.BAD_REQUEST,
            BadRequestSchema().load(
                {
                    GenericConstants.SUCCESS: False,
                    GenericConstants.ERRORS: errors
                }
            )
        )

    def _validate_json_body(self, body: bytes) -> Any:
        try:
            if body == b'' or body == b'{}':
                raise json.JSONDecodeError(
                    msg=MessagesConstants.MSG_EMPTY_REQUEST_BODY,
                    doc='{}',
                    pos=0
                )
            return json_decode(body)
        except json.JSONDecodeError as decode_error:
            self.logger.warning(msg=str(decode_error))
            return decode_error

    def _set_authentication_context(self) -> None:
        _encoded_token = self._fetch_encoded_bearer_token()
        try:
            decoded_token = TokenGenerator.decode(value=_encoded_token)
            if (
                FieldNameConstants.USER_ID not in decoded_token
                or decoded_token[FieldNameConstants.USER_ID] is None
            ):
                raise jwt.exceptions.DecodeError(
                    MessagesConstants.MSG_INVALID_USER_ID
                )
            self.user_id = UUID(decoded_token[FieldNameConstants.USER_ID])

        except jwt.exceptions.DecodeError as decode_error:
            self.logger.warning(msg=str(decode_error))
            return self._raise_unauthorized_request()

    def _fetch_encoded_bearer_token(self) -> Optional[str]:
        # Fetch Token From Headers
        _bearer_token = self._fetch_authorization_and_extract_bearer_token()
        if _bearer_token is None:
            # Raise Unauthorized Request
            return self._raise_unauthorized_request()
        return _bearer_token

    def _fetch_authorization_and_extract_bearer_token(self) -> Optional[str]:
        _auth_token: Any = self.request.headers.get(
            GenericConstants.HEADER_AUTHORIZATION,
            default=''
        )
        return AuthenticationBearerTokenParser.extract(value=_auth_token)

    def _raise_unauthorized_request(self):
        self.build_response(HTTPStatus.UNAUTHORIZED)

    def _set_log_context(self) -> None:
        _load_context: Dict[Any, Any] = self._prepare_log_context()
        Logger.set_log_context(**_load_context)

        Logger.log(
            self.logger,
            logging.DEBUG,
            include_context=True,
            message=GenericConstants.REQUEST
        )

    def _prepare_log_context(self) -> Dict[Any, Any]:
        _context: Dict[Any, Any] = dict()
        _context[
            GenericConstants.REQUEST_ID
        ] = self.request_id
        _context[
            GenericConstants.METHOD
        ] = self.request.method
        _context[
            GenericConstants.URI
        ] = self.request.uri
        _context[
            GenericConstants.IP
        ] = self.request.remote_ip
        return _context

    def build_response(self, status: int, data: Any = None) -> None:
        if data is not None:
            self._json_response(status, data)
        else:
            self._status_response(status)

    def _status_response(self, status: int):
        self.set_status(status)
        self.finish()

    def _json_response(self, status: int, data: Any):
        """Helper method for sending response containing json data
        """
        self.set_header(
            HttpConstants.HEADER_CONTENT_TYPE,
            HttpConstants.MIME_TYPE_JSON
        )
        self.set_status(status)
        self.write(json.dumps(data, default=str))
        self.finish()
