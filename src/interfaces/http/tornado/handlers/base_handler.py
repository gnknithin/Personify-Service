import json
import logging
import traceback
from http import HTTPStatus
from types import TracebackType
from typing import Any, Awaitable, Dict, List, Optional, Type

import tornado
from infra.constants._string import GenericConstants, HttpConstants, MessagesConstants
from infra.generator.identity import IdentityGenerator
from infra.logging.logger import Logger
from interfaces.http.tornado.schemas.base_schema import BadRequestSchema
from tornado.escape import json_decode
from tornado.web import HTTPError, RequestHandler


class BaseRequestHandler(RequestHandler):
    payload = None
    request_id = None

    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any]
    ) -> None:

        self.logger = logger
        self.schema_method_validators = schema_method_validators
        self.request_id = IdentityGenerator.get_random_id()

    def prepare(self) -> Optional[Awaitable[None]]:
        _load_context : Dict[Any,Any] = dict()
        _load_context[
            GenericConstants.REQUEST_ID
        ] = self.request_id
        _load_context[
            GenericConstants.METHOD
        ] = self.request.method
        _load_context[
            GenericConstants.URI
        ] = self.request.uri
        _load_context[
            GenericConstants.IP
        ] = self.request.remote_ip

        Logger.set_log_context(**_load_context)

        Logger.log(
            self.logger,
            logging.DEBUG,
            include_context=True,
            message=GenericConstants.REQUEST
        )

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

    def on_finish(self) -> None:
        return super().on_finish()

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        _charset : str = f'{GenericConstants.CHARSET}={GenericConstants.UTF8}'
        _headers : str = f'{HttpConstants.MIME_TYPE_JSON}; {_charset}'
        self.set_header(
            name=HttpConstants.HEADER_CONTENT_TYPE,
            value=_headers
        )
        _body : Dict[Any,Any] = dict()
        _body[
            GenericConstants.METHOD
        ] = self.request.method
        _body[
            GenericConstants.URI
        ] = self.request.path
        _body[
            GenericConstants.CODE
        ] = status_code
        _body[
            GenericConstants.MESSAGE
        ] = self._reason

        Logger.set_log_context(reason=self._reason)

        if 'exc_info' in kwargs:
            exc_info = kwargs['exc_info']
            Logger.set_log_context(exc_info=exc_info)
            if self.settings.get('serve_traceback'):
                # in debug mode, send a traceback
                trace = '\n'.join(traceback.format_exception(*exc_info))
                _body['trace'] = trace

        self.finish(_body)

    def log_exception(
            self,
            typ: Optional[Type[BaseException]],
            value: Optional[BaseException],
            tb: Optional[TracebackType]
        ) -> None:
        if isinstance(value, HTTPError):
            if value.log_message:
                msg = value.log_message % value.args
                Logger.log(
                    tornado.log.gen_log,
                    logging.WARNING,
                    status=value.status_code,
                    request_summary=self._request_summary(),
                    message=msg
                )
        else:
            Logger.log(
                tornado.log.app_log,
                logging.ERROR,
                message=GenericConstants.UNCAUGHT_EXCEPTION,
                request_summary=self._request_summary(),
                request=repr(self.request),
                exc_info=(typ, value, tb)
            )

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
