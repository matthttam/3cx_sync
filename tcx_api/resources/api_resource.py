from tcx_api.api import API
from abc import ABC


class APIResource(ABC):
    def __init__(self, api: API):
        self.api = api
