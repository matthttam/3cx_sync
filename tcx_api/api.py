import requests
from abc import ABC, abstractmethod


class API(ABC):
    @abstractmethod
    def get(endpoint: str, query_params: dict) -> requests.Response: ...

    @abstractmethod
    def post(self, endpoint: str, data: dict) -> requests.Response: ...

    @abstractmethod
    def authenticate(self): ...
