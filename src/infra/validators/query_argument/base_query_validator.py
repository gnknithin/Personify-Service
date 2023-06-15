import logging
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseQueryArgumentValidator(ABC):

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @abstractmethod
    def _transpose_query_arguments_with_transpose_to(
        self,
        query_args: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        '''Transpose Query Arguments based on transpose_to'''
        raise NotImplementedError

    @abstractmethod
    def _validate_query_arguments_with_business_rules(
        self,
        query_args: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        raise NotImplementedError

    @abstractmethod
    def _validate_query_arguments_with_validate_by(
        self,
        query_args: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        '''Validate all Query Arguments with specified validate_by'''

        raise NotImplementedError

    @abstractmethod
    def _validate_query_arguments(
        self,
        **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        '''Validate query arguments'''

        raise NotImplementedError

    @abstractmethod
    def _validate(
        self,
        **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        '''Validate Query Arguements with Rules'''

        raise NotImplementedError

    def validate(
        self,
        **kwargs: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        '''
        Validate query arguments with Validation Rules,
        Business Rules and Transformation Rules
    '''

        return self._validate(**kwargs)
