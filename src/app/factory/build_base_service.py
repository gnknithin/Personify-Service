from abc import abstractmethod
from typing import Any

from bootstrap import ApplicationBootstrap


class BaseServiceFactory():
    def __init__(self, bootstrap: ApplicationBootstrap) -> None:
        self._bootstrap = bootstrap

    @abstractmethod
    def build(self, scope: str) -> Any:
        raise NotImplementedError
