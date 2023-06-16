import logging
from typing import Any, Dict, List, Optional, Type, Union
from uuid import UUID

from app.base_generic_service import BaseGenericService
from domain.user_model import UserModel
from infra.constants._string import (
    ColumnComparisionOperatorConstant,
    FieldNameConstants,
    MessagesConstants,
)
from infra.constants._type import TSQLEntityModel
from infra.data.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork
from infra.generator.hashing import HashGenerator
from infra.generator.token import TokenGenerator
from sqlalchemy.exc import IntegrityError


class UserService(BaseGenericService[UserModel]):
    def __init__(
        self,
        logger: logging.Logger,
        uow: PostgresUnitOfWork[TSQLEntityModel],
        model_type: Type[UserModel],
    ) -> None:
        super().__init__(logger=logger, uow=uow, model_type=model_type)

    def createUser(self, data: UserModel) -> Union[None, UUID]:
        try:
            data.password = HashGenerator.create(
                value=data.password
            )
            user_id = self._add(data=data)
        except IntegrityError as intgrity_error:
            # https://docs.sqlalchemy.org/en/20/errors.html#interfaceerror
            self._logger.warning(msg=f'{intgrity_error}')
            user_id = None
        return user_id

    def findByUserName(self, userName: str) -> Union[UserModel, None]:
        _column_filter_1: Dict[Any, Any] = dict()
        _column_filter_1[
            ColumnComparisionOperatorConstant.EQUAL
        ] = userName
        _filter: Dict[Any, Any] = dict()
        # Add Columns-to-Filter
        _filter[
            FieldNameConstants.USERNAME
        ] = _column_filter_1
        _result: List[UserModel] = self._get(filter_by=_filter)
        _user: Optional[UserModel] = None
        for _each in _result:
            if _each.username == userName:
                _user = _each
                break
        return _user

    def loginUserWithCredentials(self, data: UserModel) -> Union[str, List[str]]:
        _findUser = self.findByUserName(userName=data.username)
        _errors: List[str] = list()
        if _findUser is not None:
            _is_valid_password = HashGenerator.is_valid(
                hashed_value=_findUser.password,
                value=data.password
            )
            if _is_valid_password:
                _encode: Dict[Any, Any] = dict()
                _encode[FieldNameConstants.USER_ID] = str(_findUser._id)
                return TokenGenerator.encode(data=_encode)
            else:
                _errors.append(MessagesConstants.MSG_INVALID_PASSWORD)
        else:
            _errors.append(f'Account with {data.username} does not exist')
        return _errors

    def getUserById(
        self, user_id: UUID
    ) -> Union[UserModel, None]:
        return self._get_by_key(key=user_id)

    def deleteUser(self, user_id: UUID) -> bool:
        return self._remove(key=user_id)
