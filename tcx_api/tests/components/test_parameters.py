from abc import ABC
from tcx_api.components.parameters import Parameters
import pytest


class TestParameters:

    def test_parameters_is_abc(self):
        assert issubclass(Parameters, ABC)
