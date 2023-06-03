from typing import Any, Dict

from domain.base_model import BaseModel
from infra.constants._string import FieldNameConstants
from marshmallow import fields, pre_dump, pre_load


class ContactModel(BaseModel):
    contact_id = fields.String(required=False, allow_none=True)
    user_id = fields.UUID(required=True, allow_none=False)
    full_name = fields.String(required=True, allow_none=False)
    birthday = fields.Date(required=False, allow_none=True)
    mobile = fields.String(required=False, allow_none=True)
    email = fields.Email(required=False, allow_none=True)

    @pre_load
    def copy_id_to_contact_id(
        self, in_data: Dict[Any, Any], **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        if FieldNameConstants.OBJECT_ID in in_data:
            in_data[FieldNameConstants.CONTACT_ID] = str(
                in_data[FieldNameConstants.OBJECT_ID]
            )
        return in_data

    @pre_dump
    def remove_contact_id(
        self, in_data: Dict[Any, Any], **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        if (
            (FieldNameConstants.CONTACT_ID in in_data)
            and (in_data[FieldNameConstants.CONTACT_ID] is not None)
            and (isinstance(in_data[FieldNameConstants.CONTACT_ID], str))
        ):
            del in_data[
                FieldNameConstants.CONTACT_ID
            ]
        return in_data
