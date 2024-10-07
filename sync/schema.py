from tcx_api.components.schemas.pbx import User
from typing import Optional


class SourceSchema:
    _comparison_properties: list = None

    def __eq__(self, other):
        if not self._comparison_properties:
            return super().__eq__(other)
        for prop in self._comparison_properties:
            if getattr(self, prop) != getattr(other, prop):
                return False
        return True


class CSVUser(SourceSchema, User):
    Id: Optional[int] = None
