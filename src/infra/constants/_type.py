from typing import TypeVar

from domain.base_model import BaseModel, BaseSQLModel

TEntity = TypeVar(
    "TEntity", bound=None, covariant=False,
    contravariant=False)  # Can be anything


TSQLEntityModel = TypeVar("TSQLEntityModel", bound=BaseSQLModel)
TEntityModel = TypeVar("TEntityModel", bound=BaseModel)
