import pytest

from requests import Response, Session, HTTPError
from tcx_api.exceptions import APIAuthenticationError
from tcx_api.tcx_api_connection import (
    AuthenticationToken,
    TCX_API_Connection,
)
from unittest.mock import MagicMock
from tcx_api.components.parameters import ListParameters


class TestTCX_API_Connection:
    @pytest.fixture
    def mock_get_response(self):
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = None
        return mock_response

    @pytest.fixture
    def mock_post_response(self):
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = None
        return mock_response

    @pytest.fixture
    def mock_session(self, mock_get_response, mock_post_response):
        mock_session = MagicMock(spec=Session)
        mock_session.get.return_value = mock_get_response
        mock_session.post.return_value = mock_post_response
        return mock_session

    @pytest.fixture
    def authentication_token(self):
        return AuthenticationToken(
            token_type="bearer",
            expires_in=60,
            access_token="EXAMPLE_TOKEN",
            refresh_token="EXAMPLE_REFRESH_TOKEN",
        )

    @pytest.fixture
    def api_connection(self, mock_session, authentication_token):
        api_connection = TCX_API_Connection(server_url="http://example.com")
        api_connection.session = mock_session
        api_connection.token = authentication_token
        return api_connection

    def test_get_api_endpoint_url(self, api_connection):
        endpoint = "test"
        assert (
            api_connection.get_api_endpoint_url(endpoint)
            == "http://example.com/xapi/v1/test"
        )

    def test_api_url(self, api_connection):
        assert api_connection.api_url == "http://example.com/xapi/v1"
        api_connection.api_path = "/test_path"
        assert api_connection.api_url == "http://example.com/test_path"

    def test_get_headers(self, api_connection):
        token = MagicMock()
        token.access_token = "test_token"
        api_connection.token = token
        headers = api_connection.get_headers()
        assert headers == {
            "Authorization": "Bearer test_token",
            "content-type": "application/json",
            "Accept": "application/json",
        }

    def test_get_unauthenticated_headers(self, api_connection):
        headers = api_connection.get_unauthenticated_headers()
        assert headers == {
            "Content-type": "application/json",
            "Accept": "application/json",
        }

    def test_get(self, api_connection, mock_session, mock_get_response):
        endpoint = "test_endpoint"
        params = MagicMock()
        assert api_connection.get(endpoint=endpoint, params=params) == mock_get_response
        mock_session.get.assert_called_once_with(
            url="http://example.com/xapi/v1/test_endpoint",
            params=params.model_dump.return_value,
            headers=api_connection.get_headers(),
        )
        mock_get_response.raise_for_status.assert_called_once()

    def test_post(self, api_connection, mock_session, mock_post_response):
        endpoint = "test_endpoint"
        data = {"key": "value"}
        assert api_connection.post(endpoint=endpoint, data=data) == mock_post_response
        mock_session.post.assert_called_once_with(
            url="http://example.com/xapi/v1/test_endpoint", data=data
        )
        mock_post_response.raise_for_status.assert_called_once()

    # def test_patch(self, api_connection, mock_session):
    #    endpoint = "test_endpoint"
    #    params = MagicMock()
    #    data = {"key": "value"}
    #    response_mock = MagicMock(spec=Response)
    #    mock_session.patch.return_value = response_mock
    #    response_mock.raise_for_status.side_effect = None
    #    assert api_connection.patch(endpoint, params, data) == response_mock
    #    mock_session.patch.assert_called_once_with(
    #        url="http://example.com/xapi/v1/test_endpoint", params=params, data=data
    #    )
    #    response_mock.raise_for_status.assert_called_once()

    # def test_delete(self, api_connection, mock_session):
    #    endpoint = "test_endpoint"
    #    id = 123
    #    response_mock = MagicMock(spec=Response)
    #    mock_session.delete.return_value = response_mock
    #    response_mock.raise_for_status.side_effect = None
    #    assert api_connection.delete(endpoint, id) == response_mock
    #    mock_session.delete.assert_called_once_with(
    #        url="http://example.com/xapi/v1/test_endpoint", params=id
    #    )
    #    response_mock.raise_for_status.assert_called_once()

    def test_authenticate(self, api_connection, mock_session):
        username = "user"
        password = "pass"
        response_mock = MagicMock(spec=Response)
        response_mock.json.return_value = {
            "Token": {
                "access_token": "test_token",
                "token_type": "bearer",
                "expires_in": 60,
                "refresh_token": "test_refresh_token",
            }
        }
        mock_session.post.return_value = response_mock
        response_mock.raise_for_status.side_effect = None
        api_connection.authenticate(username, password)
        mock_session.post.assert_called_once_with(
            url="http://example.com/webclient/api/Login/GetAccessToken",
            json={"SecurityCode": "", "Username": username, "Password": password},
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        response_mock.raise_for_status.assert_called_once()
        assert api_connection.token.access_token == "test_token"

    def test_authenticate_failure(self, api_connection, mock_session):
        username = "user"
        password = "pass"
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_session.post.return_value = mock_response
        with pytest.raises(APIAuthenticationError):
            api_connection.authenticate(username, password)
        mock_session.post.assert_called_once()

    def test_refresh_authentication(
        self, api_connection, mock_session, mock_post_response
    ):
        assert api_connection.refresh_authentication() == mock_post_response
        mock_session.post.assert_called_once_with(
            url="http://example.com/webclient/api/Login/GetAccessToken",
            json={"client_id": "Webclient", "grant_type": "refresh_token"},
            headers=api_connection.get_unauthenticated_headers(),
        )
