import logging
from typing import Any, Dict, List

from bootstrap.abstract_bootstrap import AbstractBootstrap
from bootstrap.personify_bootstrap import PersonifyBootstrap
from infrastructure.constants._string import (
    ApplicationConstants,
    ConfigurationConstants,
    GenericConstants,
)
from infrastructure.logging.logger import Logger
from interfaces.web.handlers import PERSONIFY_HANDLERS
from tornado.routing import URLSpec
from tornado.web import Application, RequestHandler


class PersonifyWebApplication(Application):
    def __init__(self, bootstrap: AbstractBootstrap, debug: bool = False) -> None:
        self.settings = dict(
            autoreload=True,
            compress_response=True,
            serve_traceback=True,
            # serve_traceback=debug,
            # static_path="templates",
            bootstrap=bootstrap,
        )
        self.handlers: List[URLSpec] = PERSONIFY_HANDLERS

        super().__init__(
            handlers=self.handlers, default_host=None, transforms=None, **self.settings
        )

    def log_request(self, handler: RequestHandler) -> None:
        logger = getattr(
            handler,
            ConfigurationConstants.LOGGER,
            logging.getLogger(ApplicationConstants.SERVICE_NAME),
        )

        if handler.get_status() < 400:
            level = logging.INFO
        elif handler.get_status() < 500:
            level = logging.WARNING
        else:
            level = logging.ERROR

        Logger.log(
            logger=logger,
            lvl=level,
            include_context=True,
            message=GenericConstants.RESPONSE,
            status=handler.get_status(),
            time_ms=(1000.0 * handler.request.request_time()),
        )
        Logger.clean_log_context()

    @staticmethod
    async def run_server(personify_bootstrap: PersonifyBootstrap, port: int) -> None:
        _http_server_args: Dict[Any, Any] = dict()
        _http_server_args[GenericConstants.DECOMPRESS_REQUEST] = True

        personify_bootstrap.server = personify_bootstrap.web_application.listen(
            port=port, address="", **_http_server_args
        )
