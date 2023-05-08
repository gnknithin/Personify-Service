from argparse import Namespace
from dataclasses import dataclass

from bootstrap import ApplicationBootstrap, BaseBootstrap


@dataclass
class BaseFakeBootstrap(BaseBootstrap):
    def __init__(self, bootstrap_args: Namespace) -> None:
        super().__init__(bootstrap_args=bootstrap_args)

@dataclass
class UnitTestFakeBootstrap(BaseFakeBootstrap):

    def __init__(self, bootstrap_args: Namespace) -> None:
        super().__init__(bootstrap_args=bootstrap_args)


class IntegrationTestFakeContainer(ApplicationBootstrap):
    pass
