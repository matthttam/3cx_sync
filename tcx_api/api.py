import requests
from abc import ABC, abstractmethod
from tcx_api.components.parameters import ListParameters
from pydantic import BaseModel


class API(ABC):
    pass


#   @abstractmethod
#   def get(endpoint: str, query_params: Parameters | dict) -> requests.Response: ...
#
#   @abstractmethod
#   def post(self, endpoint: str, data: dict) -> requests.Response: ...
#
#   @abstractmethod
#   def authenticate(self): ...
#
#   @abstractmethod
#   def delete(self, endpoint: str, )
