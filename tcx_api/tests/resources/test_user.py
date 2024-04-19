import requests
from unittest.mock import MagicMock
import pytest
from pydantic import ValidationError
from tcx_api.resources.user import ListUserParameters, UserProperties
from tcx_api.components.parameters import ListParameters
from tcx_api.resources.user import UserResource
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.components.schemas.pbx import User
from tcx_api import exceptions as TCX_Exceptions


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
        with pytest.raises(ValidationError):
            test_params.skip = -1


class TestUserResource:
    @pytest.fixture
    def user_resource(self):
        return UserResource(api=MagicMock(spec=TCX_API_Connection))

    @pytest.fixture
    def simple_user(self):
        user = User(Id=1, FirstName="TestFirstName",
                    LastName="TestLastName")
        yield user

    @pytest.fixture
    def simple_user2(self):
        user = User(Id=2, FirstName="TestFirstName2",
                    LastName="TestLastName2", )
        yield user

    def test_list_user_single_success(self, user_resource, simple_user):
        # Mocking the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                simple_user.model_dump()
            ]
        }
        user_resource.api.get.return_value = mock_response

        # Calling the method under test
        params = ListUserParameters()
        users = user_resource.list_user(params)

        # Assertions
        assert len(users) == 1
        assert users[0].Id == 1
        assert users[0].FirstName == "TestFirstName"
        assert users[0].LastName == "TestLastName"

        # Asserting that the API was called with the correct parameters
        user_resource.api.get.assert_called_once_with("Users", params)

    def test_list_user_multiple_success(self, user_resource, simple_user, simple_user2):
        # Mocking the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                simple_user.model_dump(),
                simple_user2.model_dump(),
            ]
        }
        user_resource.api.get.return_value = mock_response

        # Calling the method under test
        params = ListUserParameters()
        users = user_resource.list_user(params)

        # Assertions
        assert len(users) == 2
        assert users[1].Id == 2
        assert users[1].FirstName == "TestFirstName2"
        assert users[1].LastName == "TestLastName2"

        # Asserting that the API was called with the correct parameters
        user_resource.api.get.assert_called_once_with("Users", params)

    def test_list_user_failure(self, user_resource):
        # Mocking the API response to simulate an error
        user_resource.api.get.side_effect = requests.HTTPError

        # Calling the method under test
        params = ListUserParameters()
        with pytest.raises(TCX_Exceptions.UserListError):
            users = user_resource.list_user(params)

        # Asserting that the API was called with the correct parameters
        user_resource.api.get.assert_called_once_with("Users", params)

    def test_get_user_success(self, user_resource, simple_user):
        id = 1
        mock_response = MagicMock()
        mock_response.json.return_value = simple_user.model_dump()
        user_resource.api.get.return_value = mock_response

        params = ListUserParameters()
        user = user_resource.get_user(id=id, params=params)

        assert isinstance(user, User)
        assert user.FirstName == "TestFirstName"
        assert user.LastName == "TestLastName"

        user_resource.api.get.assert_called_once_with(
            endpoint=f"Users({id})", params=params
        )

    def test_get_user_failure(self, user_resource):
        id = 1
        user_resource.api.get.side_effect = requests.HTTPError

        params = ListUserParameters()
        with pytest.raises(TCX_Exceptions.UserGetError):
            user = user_resource.get_user(id=id, params=params)

        user_resource.api.get.assert_called_once_with(
            endpoint=f"Users({id})", params=params
        )
