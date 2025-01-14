import requests
import time

from typing import NamedTuple, Optional

from tcx_api.exceptions import APIAuthenticationError
from tcx_api.api import API
from tcx_api.components.parameters import QueryParameters


class AuthenticationToken(NamedTuple):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str


class TCX_API_Connection(API):
    default_headers = {"Content-type": "application/json", "Accept": "application/json"}

    def __init__(self, *args, server_url, api_path="/xapi/v1", **kwargs):
        self.server_url = server_url
        self.api_path = api_path
        self.session = requests.Session()
        self.token_expiry_time = 0

    @property
    def api_url(self):
        return self.server_url + self.api_path

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = AuthenticationToken(**token)
        self._update_token_expiry_time(self.token.expires_in)

    def get_api_endpoint_url(self, endpoint):
        return self.api_url + "/" + endpoint

    def get(self, endpoint: str, params: QueryParameters | None = None) -> requests.Response:
        request_params = params.model_dump(exclude_none=True, by_alias=True) if params else None
        return self._make_request(
            "get", endpoint, params=request_params
        )

    def post(self, endpoint: str, data: dict) -> requests.Response:
        """
        Sends a POST request to the specified endpoint with the given data.

        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (dict): The data to be sent in the body of the POST request.

        Returns:
            requests.Response: The response object from the POST request.
        """
        return self._make_request("post", endpoint, json=data)

    def patch(self, endpoint: str, data: dict) -> requests.Response:
        """
        Sends a PATCH request to the specified endpoint with the given data.

        Args:
            endpoint (str): The API endpoint to send the PATCH request to.
            data (dict): The data to be sent in the PATCH request.

        Returns:
            requests.Response: The response object from the PATCH request.
        """
        return self._make_request("patch", endpoint, json=data)

    def delete(self, endpoint: str, id: int) -> requests.Response:
        """
        Sends a DELETE request to the specified endpoint with the given ID.

        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
            id (int): The ID of the resource to delete.

        Returns:
            requests.Response: The response object from the DELETE request.
        """
        return self._make_request("delete", endpoint, params=id)

    def authenticate(self, username, password):
        """
        Authenticates the user with the given username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Raises:
            APIAuthenticationError: If the authentication request fails.

        Sets:
            self.token (str): The access token received from the server.
        """
        data = {"SecurityCode": "", "Username": username, "Password": password}
        try:
            response = self.session.post(
                url=self.server_url + "/webclient/api/Login/GetAccessToken",
                json=data,
                headers=self._get_headers(),
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            raise APIAuthenticationError(e)
        self.token = response.json().get("Token", {})

    def _refresh_access_token(self):
        # Get Access Token
        data = {
            "client_id": "Webclient",
            "grant_type": "refresh_token",
            "refresh_token": self.token.refresh_token,
        }
        try:
            response = self.session.post(
                url=self.server_url + "/connect/token",
                data=data,
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            raise APIAuthenticationError(e)
        self.token = response.json()

    def _is_token_expired(self, buffer: Optional[int] = 5) -> bool:
        expiration_check_time = self.token_expiry_time - buffer
        return time.time() > expiration_check_time

    def _update_token_expiry_time(self, expires_in: int) -> None:
        self.token_expiry_time = time.time() + expires_in

    def _get_headers(self) -> dict:
        """
        Generate HTTP headers for API requests.

        This method creates a copy of the default headers and adds an
        Authorization header if an access token is available.

        Returns:
            dict: A dictionary containing the HTTP headers.
        """
        headers = self.default_headers.copy()
        if self.token.access_token:
            headers["Authorization"] = f"Bearer {self.token.access_token}"
        return headers

    def _make_request(self, method, endpoint, **kwargs):
        """
        Makes an HTTP request to the specified API endpoint.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to send the request to.
            **kwargs: Additional arguments to pass to the request (e.g., params, data, json).

        Returns:
            requests.Response: The response object from the HTTP request.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = self.get_api_endpoint_url(endpoint)
        if self._is_token_expired():
            self._refresh_access_token()

        response = self.session.request(
            method, url, headers=self._get_headers(), **kwargs
        )
        response.raise_for_status()
        return response
