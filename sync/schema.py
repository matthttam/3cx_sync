from threecxapi.components.schemas.pbx import User
from typing import Optional


class SourceSchema:
    _comparison_properties: list = None

    @classmethod
    def set_comparison_properties(cls, properties: list[str]) -> None:
        if not isinstance(properties, list):
            raise TypeError("Comparison properties must be a list of strings.")
        cls._comparison_properties = properties

    def __eq__(self, other):
        if not self._comparison_properties:
            return super().__eq__(other)
        for prop in self._comparison_properties:
            if getattr(self, prop) != getattr(other, prop):
                return False
        return True


class CSVUser(SourceSchema, User):
    Id: Optional[int] = None
