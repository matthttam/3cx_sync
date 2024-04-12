import pytest
from tcx_api.resources.user import ListUserParameters
from tcx_api.components.parameters import Parameters


class TestListUserParameters:

    def test_inherits_from_parameters(self):
        assert issubclass(ListUserParameters, Parameters)

    def test_valid_empty_parameters(self):
        test_list_user_parameters = ListUserParameters()
        assert isinstance(test_list_user_parameters, ListUserParameters)

    def test_valid_parameters(self):
        params = ListUserParameters(
            orderby="Id", select=["Id", "Groups"], expand="Groups"
        )
        assert isinstance(params, ListUserParameters)

    def test_invalid_parameters(self):
        with pytest.raises(ValueError):
            ListUserParameters(select=["does_not_exist"])

    def test_valid_top(self):
        test_params = ListUserParameters(top=1)
        assert test_params.top == 1

    def test_invalid_top(self):
        with pytest.raises(ValueError):
            test_params = ListUserParameters(top=-1)

        # test_params = ListUserParameters(top=1)
        # with pytest.raises(ValueError):
        #    test_params.top = -1

    def test_valid_skip(self):
        test_params = ListUserParameters(skip=1)
        assert test_params.skip == 1

    def test_invalid_skip(self):
        with pytest.raises(ValueError):
            test_params = ListUserParameters(skip=-1)

        # test_params = ListUserParameters(skip=1)
        # with pytest.raises(ValueError):
        #    test_params.skip = -1


if __name__ == "__main__":
    pytest.main()
