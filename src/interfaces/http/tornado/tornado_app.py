import logging
from http import HTTPStatus
from typing import Any, Dict, List

from app.factory.build_contact_service import ContactServiceFactory
from app.factory.build_user_service import UserServiceFactory
from bootstrap import ApplicationBootstrap
from infra.constants._string import (
    ApplicationConstants,
    ConfigurationConstants,
    GenericConstants,
    MessagesConstants,
)
from infra.constants._url import APIEndpointV1, HandlerConstants
from infra.logging.logger import Logger
from interfaces.http.tornado.handlers.default_handler import DefaultRequestHandler
from interfaces.http.tornado.handlers.health_handler import HealthHandler
from interfaces.http.tornado.handlers.v1.contact_handler import UserContactHandler
from interfaces.http.tornado.handlers.v1.signin_handler import UserSignInHandler
from interfaces.http.tornado.handlers.v1.signup_handler import UserSignUpHandler
from interfaces.http.tornado.schemas.v1.contact_schema import CreateContactSchema
from interfaces.http.tornado.schemas.v1.user_schema import SignInSchema, SignUpSchema
from tornado.web import Application, RequestHandler


def log_function(handler: RequestHandler) -> None:
    logger = getattr(
        handler,
        ConfigurationConstants.LOGGER,
        logging.getLogger(ApplicationConstants.SERVICE_NAME)
    )

    if handler.get_status() < 400:
        level = logging.INFO
    elif handler.get_status() < 500:
        level = logging.WARNING
    else:
        level = logging.ERROR

    Logger.log(
        logger,
        level,
        include_context=True,
        message=GenericConstants.RESPONSE,
        status=handler.get_status(),
        time_ms=(1000.0 * handler.request.request_time())
    )
    Logger.clean_log_context()


class MainApplication(Application):
    def __init__(
        self,
        bootstrap: ApplicationBootstrap,
        debug: bool
    ) -> None:

        _default_handler_args: Dict[Any, Any] = dict()
        _default_handler_args[
            GenericConstants.STATUS_CODE
        ] = HTTPStatus.NOT_FOUND
        _default_handler_args[
            GenericConstants.MESSAGE
        ] = MessagesConstants.MSG_UNKNOWN_ENDPOINT
        _default_handler_args[
            ConfigurationConstants.LOGGER
        ] = bootstrap.logger

        self.settings = dict(
            autoreload=True,
            compress_response=True,
            log_function=log_function,
            serve_traceback=debug,
            default_handler_class=DefaultRequestHandler,
            default_handler_args=_default_handler_args
        )

        self.handlers: List[Any] = [
            (
                HandlerConstants.HEALTH_URI,
                HealthHandler,
                dict(
                    logger=bootstrap.logger,
                    schema_method_validators={}
                )
            ),
            (
                APIEndpointV1.SIGNUP_URI,
                UserSignUpHandler,
                dict(
                    logger=bootstrap.logger,
                    schema_method_validators=dict(
                        POST=SignUpSchema
                    ),
                    service_factory=UserServiceFactory(bootstrap=bootstrap)
                )
            ),
            (
                APIEndpointV1.SIGNIN_URI,
                UserSignInHandler,
                dict(
                    logger=bootstrap.logger,
                    schema_method_validators=dict(
                        POST=SignInSchema
                    ),
                    service_factory=UserServiceFactory(bootstrap=bootstrap)
                )
            ),
            (
                APIEndpointV1.CONTACT_URI,
                UserContactHandler,
                dict(
                    logger=bootstrap.logger,
                    schema_method_validators=dict(
                        POST=CreateContactSchema
                    ),
                    service_factory=ContactServiceFactory(bootstrap=bootstrap)
                )
            )
        ]
        super().__init__(
            handlers=self.handlers,
            default_host=None,
            transforms=None,
            **self.settings
        )

    @staticmethod
    async def run_server(
        app_bootstrap: ApplicationBootstrap,
        app: Application,
        port: int
    ) -> None:
        _http_server_args: Dict[Any, Any] = dict()
        _http_server_args[
            GenericConstants.DECOMPRESS_REQUEST
        ] = True

        app_bootstrap.server = app.listen(
            port=port,
            address='',
            **_http_server_args
        )
