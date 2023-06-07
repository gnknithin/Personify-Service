import logging
import operator
from typing import Any, Dict, List, Optional, Type, Union
from uuid import UUID

from infra.constants._string import FieldNameConstants
from infra.constants._type import TSQLEntityModel
from infra.data.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class PostgresRepository(BaseRepository[TSQLEntityModel]):
    """
    A base class for Postgres repositories.
    """

    def __init__(
        self,
        logger: logging.Logger,
        session: Session,
        model_type: Type[TSQLEntityModel]
    ) -> None:
        super().__init__(logger=logger)
        self._model_type = model_type
        self._session = session

    def count(self) -> int:
        return self._session.query(self._model_type).count()

    def add(self, data: Type[TSQLEntityModel]) -> UUID:
        with self._session as session:
            session.add(data)
            session.commit()
            session.refresh(data)

        return getattr(data, FieldNameConstants.OBJECT_ID)

    def remove(self, key: UUID) -> bool:
        result = self._session.query(
            self._model_type).filter_by(_id=key).delete()

        return result == 1

    def get_by_key(self, key: UUID) -> Union[Type[TSQLEntityModel], None]:
        return self._session.get(self._model_type, key)

    def get(
        self,
        filter_by: Optional[Dict[Any, Any]] = None,
        skip_to: int = 0,
        limit_by: int = 0
    ) -> List[Type[TSQLEntityModel]]:
        query = self._session.query(self._model_type)
        if filter_by:
            for _filter_col_name, filters_dict in filter_by.items():
                for _filter_comp_operator, _filter_col_value in filters_dict.items():
                    query = query.filter(
                        getattr(operator, _filter_comp_operator)(
                            getattr(
                                self._model_type, _filter_col_name
                            ), _filter_col_value)
                    )

        return query.offset(skip_to).limit(limit_by).all()
