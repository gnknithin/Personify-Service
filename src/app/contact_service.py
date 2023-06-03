import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union
from uuid import UUID

from app.base_generic_service import BaseGenericService
from domain.contact_model import ContactModel
from infra.constants._string import FieldNameConstants
from infra.constants._type import TEntityModel
from infra.data.unit_of_work.mongo_unit_of_work import MongoUnitOfWork


class ContactService(BaseGenericService[ContactModel]):
    def __init__(
        self,
        logger: logging.Logger,
        uow: MongoUnitOfWork[TEntityModel],
        model_type: Type[ContactModel],
    ) -> None:
        super().__init__(logger=logger, uow=uow, model_type=model_type)

    def addUserContact(self, user_id: UUID, data: ContactModel) -> Union[str, None]:
        data[FieldNameConstants.USER_ID] = user_id
        data[FieldNameConstants.CREATED_AT] = datetime.utcnow()
        data[FieldNameConstants.UPDATED_AT] = datetime.utcnow()
        return self._add(data=data)

    def updateUserContact(
        self, user_id: UUID, contact_id: str,  data: ContactModel
    ) -> Union[ContactModel, None]:
        fetchUserContact = self.getUserContactById(
            user_id=user_id,
            contact_id=contact_id
        )
        if fetchUserContact is not None:
            for each in [
                FieldNameConstants.FULL_NAME,
                FieldNameConstants.BIRTHDAY,
                FieldNameConstants.MOBILE,
                FieldNameConstants.EMAIL
            ]:
                if each in data:
                    fetchUserContact[each] = data[each]

            fetchUserContact[FieldNameConstants.UPDATED_AT] = datetime.utcnow()
            return self._update(key=contact_id, data=data)
        return None

    def getUserContactById(
        self, user_id: UUID, contact_id: str
    ) -> Union[ContactModel, None]:
        return self._get_by_key(key=contact_id)

    def getUserContacts(
        self, user_id: UUID,
        skip_to: int = 0,
        limit_by: int = 10
    ) -> List[ContactModel]:
        _apply_filter: Dict[Any, Any] = dict()
        _apply_filter[
            FieldNameConstants.USER_ID
        ] = {"$eq": str(user_id)}
        return self._get(
            filter_by=_apply_filter,
            skip_to=skip_to,
            limit_by=limit_by
        )

    def deleteUserContact(self, user_id: UUID, contact_id: str) -> bool:
        return self._remove(key=contact_id)
