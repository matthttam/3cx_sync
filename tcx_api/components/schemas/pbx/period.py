from tcx_api.components.schemas.pbx.enums import DayOfWeek as DayOfWeekEnum

from tcx_api.components.schemas.schema import Schema


class Period(Schema):
    DayOfWeek: DayOfWeekEnum = None
    Start: str = None
    Stop: str = None
