import logging
from http import HTTPStatus
from typing import Any, Dict, List

from bootstrap import ApplicationBootstrap, BaseBootstrap
from infra.constants._string import (
    ApplicationConstants,
    ConfigurationConstants,
    GenericConstants,
    MessagesConstants,
)
from infra.constants._url import HandlerConstants
from infra.logging.logger import Logger
from interfaces.http.tornado.handlers.default_handler import DefaultRequestHandler
from interfaces.http.tornado.handlers.health_handler import HealthHandler
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
        bootstrap: BaseBootstrap,
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

        self.handlers: List[Any] = list()
        self.handlers.append(
            (
                HandlerConstants.HEALTH_URI,
                HealthHandler,
                dict(
            
                    logger=bootstrap.logger,
                    schema_method_validators=dict()
                )
            )
        )

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
