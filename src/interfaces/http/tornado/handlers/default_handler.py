
import logging
from typing import Awaitable, Optional

from interfaces.http.tornado.handlers.base_handler import BaseRequestHandler
from tornado.web import HTTPError


class DefaultRequestHandler(BaseRequestHandler):
    def initialize(
            self,
            status_code: int,
            message: str,
            logger: logging.Logger
        ) -> None:
        self.logger = logger
        self.set_status(status_code, reason=message)

    def prepare(
            self
        ) -> Optional[Awaitable[None]]:
        _log_msg = "request uri: %s"
        raise HTTPError(
            self._status_code,
            _log_msg,
            self.request.uri,
            reason=self._reason
        )
