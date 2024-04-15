from abc import ABC
from tcx_api.components.parameters import ListParameters
import pytest


class TestParameters:

    def test_parameters_is_abc(self):
        assert issubclass(ListParameters, ABC)
