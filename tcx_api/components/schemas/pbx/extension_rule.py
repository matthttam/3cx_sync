from tcx_api.components.schemas.pbx.destination import Destination
from tcx_api.components.schemas.pbx.schedule import Schedule


class ExtensionRule:
    def __init__(
        self,
        Id: int,
        CallerId: str = None,
        Destination: Destination = None,
        Hours: Schedule = None,
    ):
        self.Id = Id
        self.CallerId = CallerId
        self.Destination = Destination
        self.Hours = Hours
