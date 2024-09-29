import logging
from dataclasses import dataclass
from typing import Optional

from bootstrap.abstract_bootstrap import AbstractBootstrap
from dotenv import find_dotenv, load_dotenv
from tornado.httpserver import HTTPServer
from tornado.web import Application


@dataclass(
    init=False,
    repr=True,
    eq=True,
    order=True,
    unsafe_hash=False,
    frozen=False,
    match_args=False,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class PersonifyBootstrap(AbstractBootstrap):
    logger: logging.Logger
    web_application: Optional[Application] = None
    server: Optional[HTTPServer] = None

    def __init__(self) -> None:
        super().__init__()
        _ = load_dotenv(find_dotenv())
        self.logger.info("Executed to load Environment Variables")
