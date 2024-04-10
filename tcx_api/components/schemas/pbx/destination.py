from tcx_api.components.schemas.pbx.enums import DestinationType, PeerType


class Destination:
    def __init__(
        self,
        External: str = None,
        Name: str = None,
        Number: str = None,
        PeerType: PeerType = None,
        To: DestinationType = None,
    ):
        self.External = External
        self.Name = Name
        self.Number = Number
        self.PeerType = PeerType
        self.To = To
