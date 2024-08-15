from typing import Optional
from pydantic import conlist, BaseModel


class InnerError(BaseModel):
    """The structure of this object is service-specific"""


class ErrorDetails(BaseModel):
    code: str
    message: str
    target: Optional[str] = None


class MainError(BaseModel):
    code: str
    details: Optional[conlist(ErrorDetails)] = None
    innererror: Optional[InnerError] = None
    message: str
    target: Optional[str] = None


class ODataError(BaseModel):
    error: MainError
