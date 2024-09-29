from abc import ABC
import pytest
from pytest import MarkDecorator


class AbstractUnitTest(ABC):
	pytestmark: MarkDecorator = pytest.mark.unit