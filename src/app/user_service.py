import logging
from typing import Type, Union
from uuid import UUID

from app.base_generic_service import BaseGenericService
from domain.user_model import UserModel
from infra.constants._type import TSQLEntityModel
from infra.data.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork
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
            user_id = self._add(data=data)
        except IntegrityError as intgrity_error:
            # https://docs.sqlalchemy.org/en/20/errors.html#interfaceerror
            self._logger.warning(msg=f'{intgrity_error}')
            user_id = None
        return user_id

    def getUserById(
        self, user_id: UUID
    ) -> Union[UserModel, None]:
        return self._get_by_key(key=user_id)

    def deleteUser(self, user_id: UUID) -> bool:
        return self._remove(key=user_id)
