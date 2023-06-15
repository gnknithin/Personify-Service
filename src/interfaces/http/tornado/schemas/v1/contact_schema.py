from infra.constants._string import FieldNameConstants
from interfaces.http.tornado.schemas.base_schema import BaseSchema, BaseSuccessSchema
from marshmallow import EXCLUDE, fields


# TODO Add Unit Tests
class BaseContactSchema(BaseSchema):
    _id = fields.Str(required=False)
    created_at = fields.DateTime(required=False, format=FieldNameConstants.ISO)
    updated_at = fields.DateTime(required=False, format=FieldNameConstants.ISO)
    contact_id = fields.String(required=False, allow_none=True)
    user_id = fields.UUID(required=False, allow_none=False)
    full_name = fields.String(required=True, allow_none=False)
    birthday = fields.Date(required=False, allow_none=True)
    mobile = fields.String(required=False, allow_none=True)
    email = fields.Email(required=False, allow_none=True)


class ContactSchema(BaseContactSchema):
    class Meta:
        exclude = (
            FieldNameConstants.OBJECT_ID,
            FieldNameConstants.CREATED_AT,
            FieldNameConstants.UPDATED_AT,
            FieldNameConstants.CONTACT_ID,
            FieldNameConstants.USER_ID
        )
        unknown = EXCLUDE


class UserContactSchema(BaseContactSchema):
    class Meta:
        exclude = (
            FieldNameConstants.OBJECT_ID,
            FieldNameConstants.USER_ID
        )
        unknown = EXCLUDE


class UserContactDetailSchema(BaseSuccessSchema):
    data = fields.Nested(
        UserContactSchema,
        required=True,
        description='User Contact By Id'
    )


class UserContactsListSchema(BaseSuccessSchema):
    data = fields.List(
        required=True,
        cls_or_instance=fields.Nested(UserContactSchema),
        description='List of User Contacts'
    )
