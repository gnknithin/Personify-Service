from infra.constants._string import FieldNameConstants
from interfaces.http.tornado.schemas.base_schema import BaseSchema
from marshmallow import fields


class ContactSchema(BaseSchema):
    _id = fields.Str(required=False)
    created_at = fields.DateTime(required=False, format=FieldNameConstants.ISO)
    updated_at = fields.DateTime(required=False, format=FieldNameConstants.ISO)
    contact_id = fields.String(required=False, allow_none=True)
    user_id = fields.UUID(required=False, allow_none=False)
    full_name = fields.String(required=True, allow_none=False)
    birthday = fields.Date(required=False, allow_none=True)
    mobile = fields.String(required=False, allow_none=True)
    email = fields.Email(required=False, allow_none=True)
