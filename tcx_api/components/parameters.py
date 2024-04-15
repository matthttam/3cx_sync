from abc import ABC
from pydantic import BaseModel, Field


class ListParameters(BaseModel, ABC, validate_assignment=True):
    top: int = Field(None, ge=0)
    skip: int = Field(None, ge=0)
    search: str = None
    filter: str = None
    count: bool = None
    # def to_dict(self):
    #    """
    #    Convert Parameters instance to a dictionary, excluding attributes with value None.
    #    """
    #    return {k.lstrip("_"): v for k, v in asdict(self).items() if v is not None}


class GetParameters(BaseModel, ABC, validate_assignment=True):
    expand: str = None
