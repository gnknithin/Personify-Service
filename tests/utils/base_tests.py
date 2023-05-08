from abc import ABC

import aiotask_context as context
import pytest
from bootstrap import ApplicationBootstrap
from infra.parser.argument_parser import ArgumentParser
from interfaces.http.tornado.tornado_app import MainApplication
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from tests.utils.fake_bootstrap import (
    IntegrationTestFakeContainer,
    UnitTestFakeBootstrap,
)


class BaseUnitTest(ABC):
    pytestmark = pytest.mark.unit

    @pytest.fixture(autouse=True)
    def setup_boostrap(self) -> UnitTestFakeBootstrap:
        args = ['-c', './configs/development.yaml']
        return  UnitTestFakeBootstrap(
            bootstrap_args=ArgumentParser.parse_arguments(input_args=args)
        )

    @pytest.fixture(autouse=True)
    def init_bootstrap(
        self,
        setup_boostrap:UnitTestFakeBootstrap
    ) -> UnitTestFakeBootstrap:
        return setup_boostrap


class BaseIntegrationTest(ABC):
    pytestmark = pytest.mark.integration

    @pytest.fixture(autouse=True)
    def setup_boostrap(self) -> IntegrationTestFakeContainer:
        args = ['-c', './configs/test.yaml']
        return IntegrationTestFakeContainer(
            bootstrap_args=ArgumentParser.parse_arguments(input_args=args)
        )

    @pytest.fixture(autouse=True)
    def init_bootstrap(
        self,
        setup_boostrap: IntegrationTestFakeContainer
    ) -> IntegrationTestFakeContainer:
        return setup_boostrap


class MainApplicationTestSetup(AsyncHTTPTestCase):
    pytestmark = pytest.mark.e2e

    def get_app(self) -> MainApplication:
        args = ['-p', '8888', '-c', './configs/test.yaml']
        _bootstrap = ApplicationBootstrap(
            bootstrap_args=ArgumentParser.parse_arguments(input_args=args)
        )
        return MainApplication(bootstrap=_bootstrap,debug=True)

    def get_new_ioloop(self) -> IOLoop:
        instance = IOLoop.current()
        instance.asyncio_loop.set_task_factory(context.task_factory)
        return instance
