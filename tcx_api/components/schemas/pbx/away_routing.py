from tcx_api.components.schemas.pbx.destination import Destination
from tcx_api.components.schemas.schema import Schema


class AwayRouting(Schema):
    AllHoursExternal: bool = None
    AllHoursInternal: bool = None
    External: Destination = None
    Internal: Destination = None
