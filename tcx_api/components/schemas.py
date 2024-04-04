from enum import StrEnum, auto
from typing import List


class Pbx_RuleHOursType(StrEnum):
    AllHours = auto()
    OfficeHours = auto()
    OutOfOfficeHours = auto()
    SpecificHours = auto
    SpecificHoursExcludingHolidays = auto()
    OutOfSpecificHours = auto()
    OutOfSpecificHoursIncludingHolidays = auto()
    Never = auto()
    BreakTime = auto()


class Pbx_Period:
    def __init__(self) -> None:
        pass


class Pbx_Schedule:
    def __init__(
        self,
        IgnoreHolidays: bool,
        Periods: list[Pbx_Period],
        Type: List[Pbx_RuleHOursType],
    ) -> None:
        self.IgnoreHolidays = IgnoreHolidays
        self.Periods = Periods
        self.Type = Type
