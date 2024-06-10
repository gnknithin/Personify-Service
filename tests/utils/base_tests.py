from abc import ABC
from typing import Any, Dict

import aiotask_context as context
import pytest
from app.contact_service import ContactService
from app.factory.build_contact_service import ContactServiceFactory
from app.factory.build_user_service import UserServiceFactory
from app.user_service import UserService
from bootstrap import ApplicationBootstrap
from infra.constants._string import HttpConstants
from infra.parser.argument_parser import ArgumentParser
from interfaces.http.tornado.tornado_app import MainApplication
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOLoop
from tornado.testing import AsyncHTTPTestCase

from tests.utils.fake_bootstrap import (
    IntegrationTestFakeContainer,
    UnitTestFakeBootstrap,
)


class BaseUnitTest(ABC):
    pytestmark = pytest.mark.unit

    @pytest.fixture(autouse=True)
    def setup_boostrap(self) -> UnitTestFakeBootstrap:
        args = ["-c", "./configs/development.yaml"]
        return UnitTestFakeBootstrap(
            bootstrap_args=ArgumentParser.parse_arguments(input_args=args)
        )

    @pytest.fixture(autouse=True)
    def init_bootstrap(
        self, setup_boostrap: UnitTestFakeBootstrap
    ) -> UnitTestFakeBootstrap:
        return setup_boostrap


class BaseIntegrationTest(ABC):
    pytestmark = pytest.mark.integration

    @pytest.fixture(autouse=True)
    def setup_boostrap(self) -> IntegrationTestFakeContainer:
        args = ["-c", "./configs/test.yaml"]
        return IntegrationTestFakeContainer(
            bootstrap_args=ArgumentParser.parse_arguments(input_args=args)
        )

    @pytest.fixture(autouse=True)
    def init_bootstrap(
        self, setup_boostrap: IntegrationTestFakeContainer
    ) -> IntegrationTestFakeContainer:
        return setup_boostrap


class MainApplicationTestSetup(AsyncHTTPTestCase):
    pytestmark = pytest.mark.e2e
    SCOPE = "e2e-tests"
    bootstrap = None

    def get_app(self) -> MainApplication:
        args = ["-p", "8888", "-c", "./configs/test.yaml"]
        self.bootstrap = ApplicationBootstrap(
            bootstrap_args=ArgumentParser.parse_arguments(input_args=args)
        )
        return MainApplication(bootstrap=self.bootstrap, debug=True)

    def get_new_ioloop(self) -> IOLoop:
        instance = AsyncIOLoop()
        instance.asyncio_loop.set_task_factory(context.task_factory)
        return instance

    def get_user_service(self) -> UserService:
        return UserServiceFactory(bootstrap=self.bootstrap).build(scope=self.SCOPE)

    def get_contact_service(self) -> ContactService:
        return ContactServiceFactory(bootstrap=self.bootstrap).build(scope=self.SCOPE)

    def _get_headers(self) -> Dict[Any, Any]:
        _headers: Dict[Any, Any] = dict()
        _headers[HttpConstants.HEADER_CONTENT_TYPE] = HttpConstants.MIME_TYPE_JSON
        return _headers

    def runTest(self) -> None:
        pass
