from tcx_api.components.schemas.pbx.destination import Destination
from tcx_api.util import Util


class AwayRouting:
    def __init__(
        self,
        AllHoursExternal: bool = None,
        AllHoursInternal: bool = None,
        External: Destination = None,
        Internal: Destination = None,
    ) -> None:
        self.AllHoursExternal = AllHoursExternal
        self.AllHoursInternal = AllHoursInternal
        self.External = Util.instanciate_object(External, Destination)
        self.Internal = Util.instanciate_object(Internal, Destination)
