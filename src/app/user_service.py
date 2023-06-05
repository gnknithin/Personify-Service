import logging
from typing import Any, Type, Union

from app.base_generic_service import BaseSQLGenericService
from domain.user_model import UserModel
from infra.constants._type import TSQLEntityModel
from infra.data.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork


class UserService(BaseSQLGenericService[UserModel]):
    def __init__(
        self,
        logger: logging.Logger,
        uow: PostgresUnitOfWork[TSQLEntityModel],
        model_type: Type[UserModel],
    ) -> None:
        super().__init__(logger=logger, uow=uow, model_type=model_type)

    '''
    def add(self, data: UserModel) -> Union[str, None]:
        entity_id = None

        with self.unit_of_work as uow:
            entity_id = uow.repository.add(data)

        return entity_id

    def remove(self, key: Any) -> bool:
        with self.unit_of_work as uow:
            response = uow.repository.remove(key)

            return response
    '''
