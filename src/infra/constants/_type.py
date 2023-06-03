from typing import TypeVar

from domain.base_model import BaseModel

TEntity = TypeVar(
    "TEntity", bound=None, covariant=False,
    contravariant=False)  # Can be anything

TEntityModel = TypeVar("TEntityModel", bound=BaseModel)
