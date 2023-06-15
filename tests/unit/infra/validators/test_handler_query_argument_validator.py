import logging
from typing import Any, Dict

import pytest
from infra.constants._string import HandlerQueryConstants, QueryConstants
from infra.validators.query_argument.base_query_validator import (
    BaseQueryArgumentValidator,
)
from infra.validators.query_argument.handler_query_argument_validator import (
    HandlerQueryArgumentValidator,
)

from tests.utils.base_tests import BaseUnitTest


class TestHandlerQueryArgumentValidator(BaseUnitTest):

    def test_should_return_an_instance_properly(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        # Act
        sut = HandlerQueryArgumentValidator(logger=_logger)
        # Assert
        assert isinstance(sut, BaseQueryArgumentValidator)

    def test_should_parse_integer_and_return_positive_integer(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        string_positive = '+1'
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._parse_integer(string_positive)
        # Assert
        assert sut is not None
        assert isinstance(sut, int)
        assert sut == 1

    def test_should_check_parse_integer_and_return_negative_integer(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        string_negative = '-1'
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._parse_integer(string_negative)
        # Assert
        assert sut is not None
        assert isinstance(sut, int)
        assert sut == -1

    def test_should_parse_integer_and_raise_valueerror_successfully(self):
        with pytest.raises(ValueError) as exec_info:
            # Arrange
            _logger = logging.getLogger(__name__)
            string_hello = 'hello'
            # Act
            HandlerQueryArgumentValidator(
                logger=_logger)._parse_integer(string_hello)
            # Assert
            assert exec_info.type is ValueError

    def test_should_check_compare_and_return_successfully(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._compare('lt', 1, 2)
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        assert sut is True

    def test_should_check_compare_invalid_types_and_raise_typeerror_successfully(self):
        with pytest.raises(TypeError) as exec_info:
            # Arrange
            _logger = logging.getLogger(__name__)
            # Act
            HandlerQueryArgumentValidator(
                logger=_logger)._compare('lt', 1, '2')
            # Assert
            assert exec_info.type is TypeError

    def test_should_check_is_positive_integer_and_return_positive_integer(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        positive = +11
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._is_positive_integer(value=positive)
        # Assert
        assert sut is not None
        assert isinstance(sut, int)
        assert sut == 11

    def test_should_check_is_positive_integer_and_raise_valueerror_successfully(self):
        with pytest.raises(ValueError) as exec_info:
            # Arrange
            _logger = logging.getLogger(__name__)
            negative = -11
            # Act
            HandlerQueryArgumentValidator(
                logger=_logger)._is_positive_integer(value=negative)
            # Assert
            assert exec_info.type is ValueError

    def test_should_check_is_positive_integer_from_string_and_raise_typeerror(self):
        with pytest.raises(TypeError) as exec_info:
            # Arrange
            _logger = logging.getLogger(__name__)
            string_hello = 'hello'
            # Act
            HandlerQueryArgumentValidator(logger=_logger)._is_positive_integer(
                value=string_hello)
            # Assert
            assert exec_info.type is TypeError

    def test_should_build_validation_and_return_dictionary_successfully(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        valid_input = {
            QueryConstants.VALUE: 'hello',
            QueryConstants.VALIDATE_BY: 'world',
            QueryConstants.TRANSPOSE_TO: 'world'
        }
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._build_validation(**valid_input)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)

        assert QueryConstants.VALUE in sut
        assert QueryConstants.VALIDATE_BY in sut
        assert QueryConstants.TRANSPOSE_TO in sut

        assert sut[QueryConstants.VALUE] is not None
        assert sut[QueryConstants.VALIDATE_BY] is not None
        assert sut[QueryConstants.TRANSPOSE_TO] is not None

    def test_should_build_validation_with_optional_none_and_return(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        valid_input = {
            QueryConstants.VALUE: 'hello',
            QueryConstants.VALIDATE_BY: None,
            QueryConstants.TRANSPOSE_TO: None
        }
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._build_validation(**valid_input)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)

        assert QueryConstants.VALUE in sut
        assert QueryConstants.VALIDATE_BY in sut
        assert QueryConstants.TRANSPOSE_TO in sut

        assert sut[QueryConstants.VALUE] is not None
        assert sut[QueryConstants.VALIDATE_BY] is None
        assert sut[QueryConstants.TRANSPOSE_TO] is None

    def test_should_build_validation_with_none_and_return_dictionary_successfully(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        valid_input = {
            QueryConstants.VALUE: None,
            QueryConstants.VALIDATE_BY: None,
            QueryConstants.TRANSPOSE_TO: None
        }
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._build_validation(**valid_input)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)

        assert QueryConstants.VALUE in sut
        assert QueryConstants.VALIDATE_BY in sut
        assert QueryConstants.TRANSPOSE_TO in sut

        assert sut[QueryConstants.VALUE] is None
        assert sut[QueryConstants.VALIDATE_BY] is None
        assert sut[QueryConstants.TRANSPOSE_TO] is None

    def test_should_build_validation_with_empty_and_return_successfully(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        valid_input: Dict[Any, Any] = dict()
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._build_validation(**valid_input)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)

        assert QueryConstants.VALUE in sut
        assert QueryConstants.VALIDATE_BY in sut
        assert QueryConstants.TRANSPOSE_TO in sut

        assert sut[QueryConstants.VALUE] is None
        assert sut[QueryConstants.VALIDATE_BY] is None
        assert sut[QueryConstants.TRANSPOSE_TO] is None

    def test_should_validate_query_arguments_with_none_and_return_dictionary(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._validate_query_arguments()
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert len(sut) == 0

    def test_should_validate_query_arguments_with_list_and_raise_typeerror(self):
        with pytest.raises(TypeError) as exec_info:
            # Arrange
            _logger = logging.getLogger(__name__)
            # Act
            HandlerQueryArgumentValidator(
                logger=_logger)._validate_query_arguments(**list())
            # Assert
            assert exec_info.type is TypeError

    def test_should_validate_query_arguments_with_valid_args_and_return(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        string_positive = '+1'
        valid_args = {
            HandlerQueryConstants.LIMIT: string_positive,
            HandlerQueryConstants.OFFSET: string_positive,
        }
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._validate_query_arguments(**valid_args)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert HandlerQueryConstants.LIMIT in sut
        assert HandlerQueryConstants.OFFSET in sut

        assert isinstance(sut[HandlerQueryConstants.LIMIT], dict)
        assert isinstance(sut[HandlerQueryConstants.OFFSET], dict)

        assert QueryConstants.VALUE in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.VALUE in sut[HandlerQueryConstants.OFFSET]

        assert QueryConstants.VALIDATE_BY in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.VALIDATE_BY in sut[HandlerQueryConstants.OFFSET]

        assert QueryConstants.TRANSPOSE_TO in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.TRANSPOSE_TO in sut[HandlerQueryConstants.OFFSET]

    def test_should_validate_query_arguments_with_validate_by_and_return(self):
        # Arrange
        _logger = logging.getLogger(__name__)
        string_positive = '+1'

        valid_args = {
            HandlerQueryConstants.LIMIT: string_positive,
            HandlerQueryConstants.OFFSET: string_positive,
        }
        valid_input = HandlerQueryArgumentValidator(
            logger=_logger)._validate_query_arguments(**valid_args)
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger
        )._validate_query_arguments_with_validate_by(query_args=valid_input)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert HandlerQueryConstants.LIMIT in sut
        assert HandlerQueryConstants.OFFSET in sut

        assert isinstance(sut[HandlerQueryConstants.LIMIT], dict)
        assert isinstance(sut[HandlerQueryConstants.OFFSET], dict)

        assert QueryConstants.VALUE in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.VALUE in sut[HandlerQueryConstants.OFFSET]

        assert QueryConstants.VALIDATE_BY in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.VALIDATE_BY in sut[HandlerQueryConstants.OFFSET]

        assert QueryConstants.TRANSPOSE_TO in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.TRANSPOSE_TO in sut[HandlerQueryConstants.OFFSET]

        assert QueryConstants.VALIDATED_VALUE in sut[HandlerQueryConstants.LIMIT]
        assert QueryConstants.VALIDATED_VALUE in sut[HandlerQueryConstants.OFFSET]

    def test_should_transpose_query_arguments_with_transpose_to_and_return(self):
        _logger = logging.getLogger(__name__)
        query_args = {
            HandlerQueryConstants.LIMIT: {
                QueryConstants.VALIDATED_VALUE: 11,
                QueryConstants.TRANSPOSE_TO: HandlerQueryConstants.LIMIT_BY
            },
            HandlerQueryConstants.OFFSET: {
                QueryConstants.VALIDATED_VALUE: 11,
                QueryConstants.TRANSPOSE_TO: HandlerQueryConstants.SKIP_TO
            },
        }
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger
        )._transpose_query_arguments_with_transpose_to(query_args=query_args)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert HandlerQueryConstants.LIMIT_BY in sut
        assert isinstance(sut[HandlerQueryConstants.LIMIT_BY], int)
        assert HandlerQueryConstants.SKIP_TO in sut
        assert isinstance(sut[HandlerQueryConstants.SKIP_TO], int)

    def test_should_check_validate_for_negative_offset_and_raise_valueerror(self):
        with pytest.raises(ValueError) as exec_info:
            # Arrange
            _logger = logging.getLogger(__name__)
            query_args = {
                HandlerQueryConstants.LIMIT: '11',
                HandlerQueryConstants.OFFSET: '-11',
            }
            # Act
            HandlerQueryArgumentValidator(
                logger=_logger)._validate(**query_args)
            # Assert
            assert exec_info.type is ValueError

    def test_should_check_validate_and_return_successfully(self):
        _logger = logging.getLogger(__name__)
        query_args = {
            HandlerQueryConstants.LIMIT: '11',
            HandlerQueryConstants.OFFSET: '11',
        }
        # Act
        sut = HandlerQueryArgumentValidator(
            logger=_logger)._validate(**query_args)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert HandlerQueryConstants.LIMIT_BY in sut
        assert isinstance(sut[HandlerQueryConstants.LIMIT_BY], int)
        assert HandlerQueryConstants.SKIP_TO in sut
        assert isinstance(sut[HandlerQueryConstants.SKIP_TO], int)
