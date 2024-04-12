from abc import ABC
from dataclasses import dataclass


@dataclass
class Parameters(ABC):
    pass


# def __init__(
#    self,
#    top: int = None,
#    skip: int = None,
#    count: bool = None,
#    filter: str = None,
#    search: str = None,
# ):
#    self.top = top
#    self.skip = skip
#    self.count = count
#    self.filter = filter
#    self.search = search

# @property
# def top(self):
#    return self._top


#
# @top.setter
# def top(self, value):
#    if value is not None and value < 0:
#        raise ValueError("top must be >= 0")
#    self._top = value
#
# @property
# def skip(self):
#    return self._skip
#
# @skip.setter
# def skip(self, value):
#    if value is not None and value < 0:
#        raise ValueError("skip must be >= 0")
#    self._skip = value
#
