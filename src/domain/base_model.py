from datetime import datetime
from typing import Any, Dict

from bson import ObjectId
from infra.constants._string import FieldNameConstants
from marshmallow import Schema, fields, pre_dump, pre_load


class BaseModel(Schema):
    _id = fields.Str(required=False)
    created_at = fields.DateTime(required=False, format=FieldNameConstants.ISO)
    updated_at = fields.DateTime(required=False, format=FieldNameConstants.ISO)

    @pre_load
    def convert_object_id_to_string(
        self, in_data: Dict[Any, Any], **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        if (
            (FieldNameConstants.OBJECT_ID in in_data)
            and (in_data[FieldNameConstants.OBJECT_ID] is not None)
            and (isinstance(in_data[FieldNameConstants.OBJECT_ID], ObjectId))
        ):
            in_data[
                FieldNameConstants.OBJECT_ID
            ] = str(
                in_data[FieldNameConstants.OBJECT_ID]
            )
        return in_data

    @pre_dump
    def remove_id_of_type_string(
        self, in_data: Dict[Any, Any], **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        if (
            (FieldNameConstants.OBJECT_ID in in_data)
            and (in_data[FieldNameConstants.OBJECT_ID] is not None)
            and (isinstance(in_data[FieldNameConstants.OBJECT_ID], str))
        ):
            del in_data[
                FieldNameConstants.OBJECT_ID
            ]
        return in_data

    # @pre_dump
    # def check_created_at(
    #     self, in_data: Dict[Any, Any], **kwargs: Dict[Any, Any]
    # ) -> Dict[Any, Any]:
    #     if (FieldNameConstants.CREATED_AT not in in_data):
    #         in_data[FieldNameConstants.CREATED_AT] = datetime.utcnow()
    #     return in_data

    # @pre_dump
    # def check_updated_at(
    #     self, in_data: Dict[Any, Any], **kwargs: Dict[Any, Any]
    # ) -> Dict[Any, Any]:
    #     if FieldNameConstants.UPDATED_AT not in in_data:
    #         in_data[FieldNameConstants.UPDATED_AT] = datetime.utcnow()
    #     return in_data
