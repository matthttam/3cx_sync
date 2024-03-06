import json
import requests


class Api:
    def __init__(self, *args, server_url, **kwargs):
        self.server_url = server_url
        # self.scheme = kwargs["scheme"]
        # self.server = kwargs["server"]
        # self.port = kwargs["port"]
        self.api_path = "/xapi/v1"

    # @property
    # def server_url(self):
    #    return self.scheme + "://" + self.server + ":" + self.port

    @property
    def api_url(self):
        return self.server_url + self.api_path

    def get_api_endpoint_url(self, endpoint):
        return self.api_url + "/" + endpoint

    def get(self, endpoint: str, query_params: dict):
        return requests.get(self.get_api_endpoint_url(endpoint), params=query_params)

    def post(self, endpoint: str, data):
        return requests.post(self.get_api_endpoint_url(endpoint), data=data)

    def authenticate(self, username, password):
        # Get Access Token
        data = {"SecurityCode": "", "Username": username, "Password": password}
        # data = json.dumps(data_dict, indent=4)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = requests.post(
            self.server_url + "/webclient/api/Login/GetAccessToken",
            json=data,
            headers=headers,
        )
        print(response)
