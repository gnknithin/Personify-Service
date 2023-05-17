from random import choice
from typing import Any, Dict, List

from infra.constants._string import GenericConstants


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
        return choice([True,False])


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