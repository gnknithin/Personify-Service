import logging
import operator
from typing import Any, Dict, Optional

from infra.constants._string import (
    HandlerQueryConstants,
    MessagesConstants,
    QueryConstants,
)
from infra.validators.query_argument.base_query_validator import (
    BaseQueryArgumentValidator,
)


class HandlerQueryArgumentValidator(BaseQueryArgumentValidator):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)

    BUSINESS_RULE: Dict[Any, Any] = dict()

    def _parse_integer(self, value: str) -> int:
        '''parse input value to integer'''
        return int(value)

    def _is_positive_integer(self, value: int) -> int:
        '''Check whether positive integer or raise ValueError'''
        if value < 0:
            raise ValueError(MessagesConstants.MSG_INVALID_NEGATIVE_INTEGER)
        return value

    def _build_validation(
        self, value: Optional[Any] = None,
        validate_by: Optional[Any] = None,
        transpose_to: Optional[Any] = None
    ) -> Dict[Any, Any]:
        _buid: Dict[Any, Any] = dict()
        _buid[QueryConstants.VALUE] = value
        _buid[QueryConstants.VALIDATE_BY] = validate_by
        _buid[QueryConstants.TRANSPOSE_TO] = transpose_to
        return _buid

    def _compare(self, *args: Any) -> bool:
        '''
        Standard operators comparision

        Parameters:
            args[0] : method_name
            args[1] : value_1
            args[2] : value_2
        Returns:
            True or False
        Raises:
            ValueError => if Values are of NOT same type
        '''
        return getattr(operator, args[0])(args[1], args[2])

    def _validate_query_arguments(self, **kwargs: Any) -> Dict[Any, Any]:
        '''Validate query arguments'''
        validated_query_args: Dict[Any, Any] = dict()
        if len(kwargs) == 0:

            return validated_query_args

        elif not isinstance(kwargs, dict):

            self._logger.warning(MessagesConstants.MSG_INVALID_QUERY_ARGUMENTS)

            raise ValueError(MessagesConstants.MSG_INVALID_QUERY_ARGUMENTS)

        if (
            (HandlerQueryConstants.LIMIT in kwargs)
            and (kwargs[HandlerQueryConstants.LIMIT] is not None)
        ):

            value = self._parse_integer(
                kwargs[HandlerQueryConstants.LIMIT])

            validated_query_args[HandlerQueryConstants.LIMIT] = self._build_validation(
                value=value,
                validate_by=self._is_positive_integer,
                transpose_to=HandlerQueryConstants.LIMIT_BY
            )

        if (
            (HandlerQueryConstants.OFFSET in kwargs)
            and (kwargs[HandlerQueryConstants.OFFSET] is not None)
        ):

            value = self._parse_integer(
                kwargs[HandlerQueryConstants.OFFSET])

            validated_query_args[HandlerQueryConstants.OFFSET] = self._build_validation(
                value=value,
                validate_by=self._is_positive_integer,
                transpose_to=HandlerQueryConstants.SKIP_TO
            )

        return validated_query_args

    def _validate_query_arguments_with_validate_by(
        self,
        query_args: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        '''Validates query arguments with validation rules'''
        for key, element in query_args.items():

            validate_by = element.get(QueryConstants.VALIDATE_BY, None)

            if validate_by is not None:

                validate_by = validate_by(element[QueryConstants.VALUE])

            else:

                validate_by = element.get(QueryConstants.VALUE, None)

            query_args[key][QueryConstants.VALIDATED_VALUE] = validate_by

        return query_args

    def _validate_query_arguments_with_business_rules(
        self,
        query_args: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        for method_name, key_names in self.BUSINESS_RULE.items():
            if (
                (
                    key_names[0] in query_args and key_names[1] in query_args
                ) and (
                    query_args[
                        key_names[0]
                    ][
                    QueryConstants.VALIDATED_VALUE
                    ] is not None and query_args[
                        key_names[1]
                    ][QueryConstants.VALIDATED_VALUE] is not None
                ) and (
                    not self._compare(
                        method_name,
                        query_args[
                            key_names[0]
                        ][QueryConstants.VALIDATED_VALUE],
                        query_args[
                            key_names[1]
                        ][QueryConstants.VALIDATED_VALUE]
                    )
                )
            ):
                raise ValueError(MessagesConstants.MSG_PARAMETERS_OUT_OF_RANGE)

        return query_args

    def _transpose_query_arguments_with_transpose_to(
        self,
        query_args: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        transposed_arguments: Dict[Any, Any] = dict()

        for key, element in query_args.items():

            validated_value = element.get(QueryConstants.VALIDATED_VALUE, None)
            tranpose_to = element.get(QueryConstants.TRANSPOSE_TO, None)

            if (
                (
                    key in [
                        HandlerQueryConstants.LIMIT,
                        HandlerQueryConstants.OFFSET
                    ]
                ) and (validated_value is not None and tranpose_to is not None)
            ):

                transposed_arguments[tranpose_to] = validated_value

        return transposed_arguments

    def _validate(
        self,
        **kwargs: Any
    ) -> Dict[Any, Any]:
        validated_query_args = self._validate_query_arguments(**kwargs)

        validated_query_args = self._validate_query_arguments_with_validate_by(
            query_args=validated_query_args,
        )

        validated_query_args = self._validate_query_arguments_with_business_rules(
            query_args=validated_query_args
        )

        validated_query_args = self._transpose_query_arguments_with_transpose_to(
            query_args=validated_query_args
        )

        return validated_query_args
