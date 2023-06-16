from infra.constants._string import MessagesConstants
from marshmallow import Schema, fields


class BaseSchema(Schema):
    ...


class BaseSuccessSchema(BaseSchema):
    success = fields.Boolean(
        required=True,
        description=MessagesConstants.MSG_VALIDITY_IN_CASE_OF_FAILURE,
        example=True,
    )


class BaseErrorSchema(BaseSchema):
    success = fields.Boolean(
        required=True,
        description=MessagesConstants.MSG_RESULT_OF_SERVICE_CALL,
        example=False
    )


class BadRequestSchema(BaseErrorSchema):

    errors = fields.List(
        cls_or_instance=fields.Str(),
        required=False,
        description=MessagesConstants.MSG_REASON_FOR_FAILED_REQUEST,
        example=[
            MessagesConstants.MSG_BAD_PARAMETER_INPUT_FORMAT
        ]
    )


class NotFoundSchema(BaseErrorSchema):
    errors = fields.List(
        cls_or_instance=fields.Str(),
        required=False,
        description=MessagesConstants.MSG_REASON_FOR_FAILED_REQUEST,
        example=[
            MessagesConstants.MSG_BAD_PARAMETER_INPUT_CONTENT
        ]
    )


class ServerErrorSchema(BaseErrorSchema):
    errors = fields.List(
        cls_or_instance=fields.Str(),
        required=False,
        description=MessagesConstants.MSG_REASON_FOR_FAILED_REQUEST,
        example=[
            MessagesConstants.MSG_SERVER_TIMEOUT
        ]
    )
