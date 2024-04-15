from tcx_api.components.schemas.pbx.destination import Destination as DestinationObject
from tcx_api.components.schemas.pbx.schedule import Schedule as ScheduleObject
from tcx_api.components.schemas.schema import Schema


class ExtensionRule(Schema):
    Id: int
    CallerId: str = None
    Destination: DestinationObject = None
    Hours: ScheduleObject = None
