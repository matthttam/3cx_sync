from tcx_api.components.schemas.pbx.period import Period as PeriodObject
from tcx_api.components.schemas.pbx.enums import RuleHoursType as RuleHoursTypeEnum
from tcx_api.components.schemas.schema import Schema
from pydantic import conlist


class Schedule(Schema):
    Type: RuleHoursTypeEnum
    IgnoreHolidays: bool = None
    Periods: conlist(PeriodObject) = None
