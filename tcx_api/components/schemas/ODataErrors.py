from typing import Optional
from pydantic import conlist


class InnerError:
    """The structure of this object is service-specific"""


class ErrorDetails:
    code: str
    message: str
    target: Optional[str] = None


class MainError:
    code: str
    details: Optional[conlist(ErrorDetails)]
    innererror: Optional[InnerError]
    message: str
    target: Optional[str] = None


class ODataError:
    error: MainError
