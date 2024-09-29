from logging import Logger

from personify.bootstrap.personify_bootstrap import PersonifyBootstrap
from tests.unit.abstract_unit_test import AbstractUnitTest


class TestPersonifyBootstrap(AbstractUnitTest):
    def test_initialization(self):
        # Arrange
        # Act
        _sut = PersonifyBootstrap()
        # Assert
        assert _sut is not None
        assert isinstance(_sut, PersonifyBootstrap)
        assert _sut.logger is not None
        assert isinstance(_sut.logger, Logger)
        assert _sut.server is None
