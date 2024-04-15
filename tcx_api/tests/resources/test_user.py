import pytest
from tcx_api.resources.user import ListUserParameters, UserProperties
from tcx_api.components.parameters import ListParameters
from pydantic import ValidationError


class TestListUserParameters:

    def test_inherits_from_parameters(self):
        assert issubclass(ListUserParameters, ListParameters)

    def test_valid_empty_parameters(self):
        test_list_user_parameters = ListUserParameters()
        assert isinstance(test_list_user_parameters, ListUserParameters)

    def test_valid_select(self):
        select = list(UserProperties)
        params = ListUserParameters(select=select)
        assert isinstance(params, ListUserParameters)

    def test_invalid_select(self):
        select = list(UserProperties)
        select.append("INVALID_VALUE")
        with pytest.raises(ValidationError):
            ListUserParameters(select=select)

    def test_valid_expand(self):
        expand = "test"
        params = ListUserParameters(expand=expand)
        assert isinstance(params, ListUserParameters)

    def test_invalid_expand(self):
        expand = 3
        with pytest.raises(ValidationError):
            ListUserParameters(expand=expand)

    def test_valid_top(self):
        test_params = ListUserParameters(top=1, skip=1)
        assert test_params.top == 1

    def test_invalid_top(self):
        with pytest.raises(ValidationError):
            test_params = ListUserParameters(top=-1)

        test_params = ListUserParameters(top=1)
        with pytest.raises(ValidationError):
            test_params.top = -1

    def test_valid_skip(self):
        test_params = ListUserParameters(skip=1)
        assert test_params.skip == 1

    def test_invalid_skip(self):
        with pytest.raises(ValidationError):
            test_params = ListUserParameters(skip=-1)

        test_params = ListUserParameters(skip=1)
        with pytest.raises(ValueError):
            test_params.skip = -1


if __name__ == "__main__":
    pytest.main()
