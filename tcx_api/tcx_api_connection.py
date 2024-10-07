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
    def get_api_endpoint_url(self, endpoint):
        return self.api_url + "/" + endpoint

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

    def is_token_expired(self, buffer: Optional[int] = 5) -> bool:
        expiration_check_time = self.token_expiry_time - buffer
        return time.time() > expiration_check_time

    def _update_token_expiry_time(self, expires_in: int) -> None:
        self.token_expiry_time = time.time() + expires_in

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token.access_token}",
            "content-type": "application/json",
            "Accept": "application/json",
        }

    def _get_unauthenticated_headers(self) -> dict:
        return {"Content-type": "application/json", "Accept": "application/json"}

    def _make_request(self, method, endpoint, **kwargs):
        url = self.get_api_endpoint_url(endpoint)
        if self.is_token_expired():
            self.refresh_access_token()

        response = self.session.request(
            method, url, headers=self._get_headers(), **kwargs
        )
        response.raise_for_status()
        return response

    def __init__(self, *args, server_url, api_path="/xapi/v1", **kwargs):
        self.server_url = server_url
        self.api_path = api_path
        self.session = requests.Session()
        self.token_expiry_time = 0

    def get(self, endpoint: str, params: QueryParameters) -> requests.Response:
        return self._make_request(
            "get", endpoint, params=params.model_dump(exclude_none=True, by_alias=True)
        )

    def post(self, endpoint: str, data: dict) -> requests.Response:
        return self._make_request("post", endpoint, json=data)

    def patch(self, endpoint: str, data: dict) -> requests.Response:
        return self._make_request("patch", endpoint, json=data)

    def delete(self, endpoint: str, id: int) -> requests.Response:
        return self._make_request("delete", endpoint, params=id)

    def authenticate(self, username, password):
        data = {"SecurityCode": "", "Username": username, "Password": password}
        try:
            response = self.session.post(
                url=self.server_url + "/webclient/api/Login/GetAccessToken",
                json=data,
                headers=self._get_unauthenticated_headers(),
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            raise APIAuthenticationError(e)
        self.token = response.json().get("Token", {})

    def refresh_access_token(self):
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
