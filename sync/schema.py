from tcx_api.components.schemas.pbx import User
from typing import Optional


class SourceSchema:
    _update_fields: list = None

    def __eq__(self, other):
        if not CSVUser._update_fields:
            return super().__eq__(other)
        for prop in CSVUser._update_fields:
            if getattr(self, prop) != getattr(other, prop):
                return False
        return True


class CSVUser(SourceSchema, User):
    Id: Optional[int] = None
