from datetime import datetime
from typing import Any, Dict

from bson import ObjectId
from infra.constants._string import FieldNameConstants
from infra.generator.identity import IdentityGenerator
from marshmallow import Schema, fields, pre_dump, pre_load
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


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


class BaseSQLModel(DeclarativeBase):
    __abstract__ = True

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class BaseSQLIdModel(BaseSQLModel):
    __abstract__ = True

    _id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False,
        default=IdentityGenerator.get_random_uuid4
    )
