from abc import ABC, abstractstaticmethod
from typing import Any


class BaseConnectionStringValidator(ABC):

    @abstractstaticmethod
    def validate(connection_string: Any) -> bool:
        raise NotImplementedError
