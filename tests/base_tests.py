from abc import ABC

import pytest


class BaseUnitTest(ABC):
    pytestmark = pytest.mark.unit