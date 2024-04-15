from abc import ABC
from tcx_api.tcx_api_connection import TCX_API_Connection
from pydantic import BaseModel, ConfigDict


class APIResource(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    endpoint: str
    api: TCX_API_Connection
