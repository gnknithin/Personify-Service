from datetime import date, datetime
from random import choice, randint
from typing import Any, Dict, List

from infra.constants._string import FieldNameConstants, GenericConstants
from infra.generator.identity import IdentityGenerator


class InitializeCoreSeed():

    @staticmethod
    def get_dict() -> Dict[Any, Any]:
        return dict()

    @staticmethod
    def get_list() -> List[Any]:
        return list()

    @staticmethod
    def get_true() -> bool:
        return True

    @staticmethod
    def get_false() -> bool:
        return False

    @staticmethod
    def get_random_bool() -> bool:
        return choice(
            [
                InitializeCoreSeed.get_true(),
                InitializeCoreSeed.get_false()
            ]
        )

    @staticmethod
    def get_datetime_utcnow() -> datetime:
        return datetime.utcnow()

    @staticmethod
    def get_date() -> date:
        return datetime.utcnow().date()

    @staticmethod
    def get_date_isoformat() -> str:
        return datetime.utcnow().date().isoformat()

    @staticmethod
    def get_datetime_utcnow_isoformat() -> str:
        return InitializeCoreSeed.get_datetime_utcnow().isoformat()

    @staticmethod
    def get_full_name(value: int) -> str:
        return f'full-name-{value}'

    @staticmethod
    def get_username(value: int) -> str:
        return f'user-{value}-name-{randint(a=1,b=100)}'

    @staticmethod
    def get_password(value: int) -> str:
        return f'user-{value}-password'

    @staticmethod
    def get_gender_male() -> str:
        return 'male'

    @staticmethod
    def get_gender_female() -> str:
        return 'female'

    @staticmethod
    def get_random_gender() -> str:
        return choice(
            [
                InitializeCoreSeed.get_gender_male(),
                InitializeCoreSeed.get_gender_female()
            ]
        )

    @staticmethod
    def get_email(value: int) -> str:
        return f'seed-{value}@personify-service.com'

    @staticmethod
    def get_mobile(value: int) -> str:
        return f'+919{value}23456789'


class BaseSuccessSchemaSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed().get_list()
        for _ in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed().get_dict()
            _d[GenericConstants.SUCCESS] = InitializeCoreSeed.get_random_bool()
            _data.append(_d)
        return _data


class BadRequestSchemaSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed().get_list()
        for each in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed().get_dict()
            _d[GenericConstants.SUCCESS] = InitializeCoreSeed.get_random_bool()
            _d[GenericConstants.ERRORS] = InitializeCoreSeed.get_list()
            _d[GenericConstants.ERRORS].append(f'Error-{each}')
            _data.append(_d)
        return _data


class BaseSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed.get_list()
        for _ in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed.get_dict()
            _d[
                FieldNameConstants.CREATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _d[
                FieldNameConstants.UPDATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _data.append(_d)
        return _data


class BaseIdSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed.get_list()
        for _ in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed.get_dict()
            _d[
                FieldNameConstants.OBJECT_ID
            ] = IdentityGenerator.get_random_id_of_object_length()
            _d[
                FieldNameConstants.CREATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _d[
                FieldNameConstants.UPDATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _data.append(_d)
        return _data


class ContactSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed.get_list()
        for each in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed.get_dict()
            _d[
                FieldNameConstants.OBJECT_ID
            ] = IdentityGenerator.get_random_id_of_object_length()
            _d[
                FieldNameConstants.CREATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _d[
                FieldNameConstants.UPDATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _d[
                FieldNameConstants.USER_ID
            ] = IdentityGenerator.get_random_uuid4()
            _d[
                FieldNameConstants.FULL_NAME
            ] = InitializeCoreSeed.get_full_name(each)
            _d[
                FieldNameConstants.BIRTHDAY
            ] = InitializeCoreSeed.get_date_isoformat()

            _d[
                FieldNameConstants.EMAIL
            ] = InitializeCoreSeed.get_email(each)

            _d[
                FieldNameConstants.MOBILE
            ] = InitializeCoreSeed.get_mobile(each)
            _data.append(_d)
        return _data


class SampleTestSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed.get_list()
        for each in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed.get_dict()
            _d[
                FieldNameConstants.CREATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow_isoformat()
            _d[
                FieldNameConstants.FULL_NAME
            ] = InitializeCoreSeed.get_full_name(each)
            _d[
                FieldNameConstants.GENDER
            ] = InitializeCoreSeed.get_random_gender()
            _d[
                FieldNameConstants.ACTIVE
            ] = InitializeCoreSeed.get_random_bool()
            _data.append(_d)
        return _data


class UserSeed():
    @staticmethod
    def create_seed(size: int) -> List[Dict[Any, Any]]:
        _data: List[Dict[Any, Any]] = InitializeCoreSeed.get_list()
        for each in range(size):
            _d: Dict[Any, Any] = InitializeCoreSeed.get_dict()
            _d[
                FieldNameConstants.CREATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow()
            _d[
                FieldNameConstants.UPDATED_AT
            ] = InitializeCoreSeed.get_datetime_utcnow()
            _d[
                FieldNameConstants.OBJECT_ID
            ] = IdentityGenerator.get_random_uuid4()
            _d[
                FieldNameConstants.USERNAME
            ] = InitializeCoreSeed.get_username(each)
            _d[
                FieldNameConstants.PASSWORD
            ] = InitializeCoreSeed.get_password(each)
            _d[
                FieldNameConstants.FULL_NAME
            ] = InitializeCoreSeed.get_full_name(each)
            _d[
                FieldNameConstants.DATE_OF_BIRTH
            ] = InitializeCoreSeed.get_date()
            _d[
                FieldNameConstants.EMAIL
            ] = InitializeCoreSeed.get_email(each)
            _data.append(_d)
        return _data
