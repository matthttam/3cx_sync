from tcx_api.tcx_api_connection import TCX_API_Connection
from .user import User
from typing import Any
from .api_resource import APIResource


class ResourceFactory:
    def __init__(self, api_connection: TCX_API_Connection):
        self.api_connection = api_connection
        self.resources = {
            "User": User(self.api_connection)  # Add other resources as needed
        }

    def get_resource(self, name: str) -> APIResource:
        if name in self.resources:
            return self.resources[name]
        else:
            raise ValueError(f"Resource '{name}' not found")
