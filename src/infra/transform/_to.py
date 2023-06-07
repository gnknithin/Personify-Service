
from typing import Any, Dict, Type, cast

from infra.constants._type import T


def to_class(c: Type[T], x: Any) -> Dict[Any, Any]:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()
