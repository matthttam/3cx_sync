from tcx_api.components.schemas.pbx.period import Period
from tcx_api.components.schemas.pbx.enums import RuleHoursType


class Schedule:
    def __init__(
        self,
        Type: RuleHoursType,
        IgnoreHolidays: bool = None,
        Periods: list[Period] = None,
    ) -> None:
        self.Type = Type
        self.IgnoreHolidays = IgnoreHolidays
        self.Periods = Periods
