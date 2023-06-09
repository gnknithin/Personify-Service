from domain.user_model import UserModel
from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


class SignUpSchema(SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_instance = True
        transient = True
        unknown = EXCLUDE

    username = auto_field()
    password = auto_field()
    full_name = auto_field()
    date_of_birth = auto_field()
    email = auto_field()


class SignInSchema(SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_instance = True
        transient = True
        unknown = EXCLUDE

    username = auto_field()
    password = auto_field()
