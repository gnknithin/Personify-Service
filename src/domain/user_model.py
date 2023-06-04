from domain.base_model import BaseSQLIdModel
from infra.constants._string import ApplicationConstants
from sqlalchemy import Column, Date, String


class UserModel(BaseSQLIdModel):
    __tablename__ = ApplicationConstants.TABLE_NAME_USERS
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=True)
