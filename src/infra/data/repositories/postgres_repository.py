import logging
from typing import Any, Dict, List, Optional, Type, Union
from uuid import UUID

from infra.constants._string import FieldNameConstants
from infra.constants._type import TSQLEntityModel
from infra.data.repositories.base_repository import BaseRepository
from sqlalchemy import BinaryExpression, ColumnOperators
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

    def _build_binary_expression(
        self,
        _comparision_operator: str,
        _column_name: str,
        _column_value: Any
    ) -> BinaryExpression[Any]:
        return getattr(
            ColumnOperators, _comparision_operator
        )(getattr(self._model_type, _column_name), _column_value)

    def _compile_filter_by(
        self,
        filter_by: Optional[Dict[Any, Any]] = None
    ) -> List[BinaryExpression[Any]]:
        _binary_expressions: List[Any] = list()
        if filter_by is not None:
            for filter_column_name, filters_dict in filter_by.items():
                for _comparision_operator, filter_column_value in filters_dict.items():
                    _compiled_expression: Any = self._build_binary_expression(
                        _comparision_operator,
                        filter_column_name,
                        filter_column_value
                    )
                    _binary_expressions.append(_compiled_expression)
        return _binary_expressions

    def get(
        self,
        filter_by: Optional[Dict[Any, Any]] = None,
        skip_to: Optional[int] = None,
        limit_by: Optional[int] = None
    ) -> List[Any]:
        """
        Get all entities.
        """
        _expression_args: List[
            BinaryExpression[Any]
        ] = self._compile_filter_by(filter_by=filter_by)
        # Execute
        with self._session as session:
            _result: List[Any] = session.query(
                self._model_type
            ).filter(*_expression_args).offset(skip_to).limit(limit_by).all()
        return _result
