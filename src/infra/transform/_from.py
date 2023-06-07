from datetime import datetime
from typing import Any

from dateutil.parser import parse


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs: Any, x: Any):
    for f in fs:
        try:
            return f(x)
        except Exception:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return parse(x)
