import requests
from typing import NamedTuple
from .api import API
from tcx_api.components.parameters import ListParameters


class TCX_API_Connection(API):
    def get_api_endpoint_url(self, endpoint):
        return self.api_url + "/" + endpoint

    @property
    def api_url(self):
        return self.server_url + self.api_path

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token.access_token}",
            "content-type": "application/json",
        }

    def __init__(self, *args, server_url, api_path="/xapi/v1", **kwargs):
        self.server_url = server_url
        self.api_path = api_path
        self.session = requests.Session()

    def get(self, endpoint: str, params: ListParameters) -> requests.Response:
        url = self.get_api_endpoint_url(endpoint)
        response = self.session.get(
            url=url,
            params=params.model_dump(exclude_none=True),
            headers=self.get_headers(),
        )
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: dict) -> requests.Response:
        url = self.get_api_endpoint_url(endpoint)
        response = self.session.post(url=url, data=data)
        response.raise_for_status()
        return response

    def patch(self, endpoint: str, params, data: dict) -> requests.Response:
        url = self.get_api_endpoint_url(endpoint)
        response = self.session.patch(url=url, params=params, data=data)
        response.raise_for_status()
        return response

    def delete(self, endpoint: str, id: int) -> requests.Response:
        url = self.get_api_endpoint_url(endpoint)
        response = self.session.delete(url=url, params=id)
        response.raise_for_status()
        return response

    def authenticate(self, username, password):
        # Get Access Token
        data = {"SecurityCode": "", "Username": username, "Password": password}
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        try:
            response = self.session.post(
                self.server_url + "/webclient/api/Login/GetAccessToken",
                json=data,
                headers=headers,
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            raise APIAuthenticationError(e.response.status_code, str(e))
        token = response.json().get("Token", {})
        self.token = AuthenticationToken(**token)

    def refresh_authentication(self):
        # Get Access Token
        data = {"client_id": "Webclient", "grant_type": "refresh_token"}
        # data = json.dumps(data_dict, indent=4)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = requests.post(
            self.server_url + "/webclient/api/Login/GetAccessToken",
            json=data,
            headers=headers,
        )
        return response


class AuthenticationToken(NamedTuple):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str


class APIAuthenticationError(Exception):
    """Exception raised when authentication fails

    Attributes:
        HTTP Response Error Message
        HTTP Response Code
    """

    def __init__(self, http_response_status_code, http_response_error_message):
        self.message = f"Authentication Failure. {http_response_error_message} ({http_response_status_code})"
        super().__init__(self.message)
