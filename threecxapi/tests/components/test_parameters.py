from abc import ABC
from threecxapi.components.parameters import ListParameters


class TestParameters:

    def test_parameters_is_abc(self):
        assert issubclass(ListParameters, ABC)
