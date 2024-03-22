import json
import requests


class API:

    def get_api_endpoint_url(self, endpoint):
        return self.api_url + "/" + endpoint

    @property
    def api_url(self):
        return self.server_url + self.api_path

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
        }

    def __init__(self, *args, server_url, api_path="/xapi/v1", **kwargs):
        self.server_url = server_url
        self.api_path = api_path
        self.access_token = ""
        self.refresh_token = ""
        self.session = requests.Session()

        self.Users = Users(self)

    def get(self, endpoint: str, query_params: dict = {}, success_codes=[200]):
        return self.session.get(
            self.get_api_endpoint_url(endpoint),
            params=query_params,
            headers=self.get_headers(),
        )

    def post(self, endpoint: str, data: dict, success_codes=[200]):
        response = self.session.post(self.get_api_endpoint_url(endpoint), data=data)
        if response.status_code in success_codes:
            return response
        return False

    def authenticate(self, username, password):
        # Get Access Token
        data = {"SecurityCode": "", "Username": username, "Password": password}
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = self.session.post(
            self.server_url + "/webclient/api/Login/GetAccessToken",
            json=data,
            headers=headers,
        )
        if response.status_code in [200]:
            token = response.json().get("Token", {})
            self.access_token = token.get("access_token", "")
            self.refresh_token = token.get("refresh_token", "")
            return True
        else:
            print("ERROR authenticating")
            return False

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


class APIResource: ...


class Users(APIResource):
    def __init__(self, api):
        self.api = api

    def get_users(self):
        try:
            # Make API call to fetch all users
            response = self.api.get("Users")
            users = response.json()["value"]
            return users
        except Exception as e:
            # Handle exceptions appropriately
            print(f"Failed to fetch users: {e}")
            return None
